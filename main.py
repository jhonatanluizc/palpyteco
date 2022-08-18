# Dataset controller
import csv
from glob import glob
import random
import urllib.request as request

# NeuralNetwork controller
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup

# App controller
from flask import Flask
app = Flask(__name__)

app_spliter = 1
app_url = "https://drive.google.com/u/0/uc?id=1qbgfDLpn4FSy165Gcgg2r7iHnmSKtPFK&export=download"
app_dataset = []
app_neuralNetwork = MLPClassifier()
app_datasetData = []
app_datasetTarget = []
app_accuracy = 0

@app.route("/")
def hello_world():
    return "hello"

@app.route("/hello")
def hello():
    from flask import render_template
    return render_template("hello.html")

@app.get('/dataset')
def get_dataset():
    global app_dataset
    global app_url
    global app_spliter

    response = request.urlopen(app_url)
    lines = [l.decode('utf-8') for l in response.readlines()]
    dataset = (list(csv.reader(lines)))[1:-1]

    prepare_dataset = []
    for data in dataset:
        prepare_dataset.append(data[2:])
    num_col = int(100/app_spliter)

    lines = []
    for item in prepare_dataset:
        inicial = 0
        final = num_col
        for x in range(app_spliter):
            lines.append(item[inicial:final])
            inicial += num_col
            final += num_col

    current_dataset = []
    for item in lines:
        data = []
        for x in range(num_col):
            if x < (num_col-1):
                valor = item[x].split('/')[0]
                data.append(int(valor))
            else:
                classe = item[x].split('/')[2]
                if(classe == "red"):
                    classe = 1
                elif(classe == "black"):
                    classe = 2
                else:
                    classe = 0      
                data.append(int(classe))
        current_dataset.append(data)

    random.shuffle(current_dataset)

    app_dataset = current_dataset
    split = len(app_dataset[0])-1
    for dados in app_dataset:
        app_datasetData.append(dados[:split])
        app_datasetTarget.append(dados[split])
   
        json = {
            "data": current_dataset,
            "lines": len(current_dataset),
            "columns": len(current_dataset[0]),
            "data": app_datasetData,
            "target": app_datasetTarget
        }
    
    return json

@app.get('/init')
def init():
    global app_neuralNetwork
    app_neuralNetwork = MLPClassifier()
    return { "reset": "OK" }

@app.get('/training')
def training():
    global app_neuralNetwork
    global app_accuracy
    global app_datasetData
    global app_datasetTarget    

    x_train, x_test, y_train, y_test = train_test_split(app_datasetData, app_datasetTarget, test_size=0.20, random_state=4)
    app_neuralNetwork.fit(x_train, y_train)
    y_pred = app_neuralNetwork.predict(x_test)
    app_accuracy = accuracy_score(y_test,y_pred)*100
    json = {"accuracy": app_accuracy}
    return json

@app.get('/predict')
def predict():
    global app_neuralNetwork
    global app_accuracy

    r = Request("https://kitblaze.com/double/?visitante=home", headers={'User-Agent': 'Mozilla/5.0'})
    html = urlopen(r)
    res = BeautifulSoup(html.read(), "html5lib")

    pdis = res.find_all("div", {"class": "pdi"})
    data = []
    for pdi in pdis:
        number = 0 if pdi.find("span") == None else int(pdi.find("span").getText())
        data.append(int(number))
    data = data[::-1]
    data = data[1:]

    y_pred = app_neuralNetwork.predict([data])
    
    if(y_pred[0] == 0):
        response = ("Branco, {}".format(y_pred[0]))
    elif((y_pred[0] == 1)):
        response = ("Vermelho, {}".format(y_pred[0]))
    else:
        response = ("Preto, {}".format(y_pred[0]))

    json = {
            "latest_numbers": [data[94], data[95], data[96], data[97], data[98]],
            "predict": response,
            "accuracy": app_accuracy
        }

    return json 