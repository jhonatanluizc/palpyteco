# Dataset controller
import csv
import random
import urllib.request as request

class Dataset():

    def get_dataset(self, url, spliter):
        response = request.urlopen(url)
        lines = [l.decode('utf-8') for l in response.readlines()]
        dataset = (list(csv.reader(lines)))[1:-1]

        prepare_dataset = []
        for data in dataset:
            prepare_dataset.append(data[2:])
        num_col = int(100/spliter)

        lines = []
        for item in prepare_dataset:
            inicial = 0
            final = num_col
            for x in range(spliter):
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

        json = {
                "data": current_dataset,
                "lines": len(current_dataset),
                "columns": len(current_dataset[0])
            }

        return json

# NeuralNetwork controller
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score
from api.controllers.dataset import Dataset
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup

class NeuralNetwork():

    neural_network = None
    accuracy = None 
    dataset = None
    dataset_data = []
    dataset_target = []

    def init(self):
        self.url = "https://drive.google.com/u/0/uc?id=1qbgfDLpn4FSy165Gcgg2r7iHnmSKtPFK&export=download"
        self.spliter = 1
        self.neural_network = MLPClassifier()
        self.accuracy = 0
        self.dataset = []
        return {"status": "OK"}

    def load_dataset(self):
        self.init()
        resquest = Dataset().get_dataset(self.url, self.spliter)
        self.dataset = resquest['data']
        split = len(self.dataset[0])-1
        for dados in self.dataset:
            self.dataset_data.append(dados[:split])
            self.dataset_target.append(dados[split])
        return {"dataset": resquest}

    def training(self):
        x_train, x_test, y_train, y_test = train_test_split(self.dataset_data, self.dataset_target, test_size=0.20, random_state=4)
        self.neural_network.fit(x_train, y_train)
        y_pred = self.neural_network.predict(x_test)
        self.accuracy = accuracy_score(y_test,y_pred)*100
        json = {"accuracy": self.accuracy}
        return json

    def predict(self):
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

        y_pred = self.neural_network.predict([data])
        
        if(y_pred[0] == 0):
            response = ("Branco, {}".format(y_pred[0]))
        elif((y_pred[0] == 1)):
            response = ("Vermelho, {}".format(y_pred[0]))
        else:
            response = ("Preto, {}".format(y_pred[0]))

        json = {
                "latest_numbers": [data[94], data[95], data[96], data[97], data[98]],
                "predict": response,
                "accuracy": self.accuracy
            }

        return json    

# App controller
from flask import Flask
from api.controllers.neural_network import NeuralNetwork

app = Flask(__name__)
neuralNetwork = NeuralNetwork()

@app.route("/")
def hello_world():
    return "hello"

@app.route("/hello")
def teste():
    from flask import render_template
    return render_template("hello.html")

@app.route("/test")
def teste():
    return neuralNetwork.get_accuracy()

@app.get('/loaddataset')
def load_dataset():
    return neuralNetwork.load_dataset()

@app.get('/training')
def training():
    return neuralNetwork.training()

@app.get('/predict')
def predict():
    return neuralNetwork.predict()