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
from asyncio.windows_events import NULL
from sklearn.datasets import load_wine
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import confusion_matrix, accuracy_score
from api.controllers.dataset import Dataset

class NeuralNetwork():

    neural_network = NULL
    accuracy = 10 
    dataset = NULL

    def test_training(self):
        dataset = load_wine()
        x_train, x_test, y_train, y_test = train_test_split(dataset.data, dataset.target, test_size=0.20, random_state=4)
        NN = MLPClassifier()
        NN.fit(x_train, y_train)
        y_pred = NN.predict(x_test)
        self.accuracy = accuracy_score(y_test,y_pred)*100
        json = {"accuracy": self.accuracy}

        return json

    def init(self):
        self.url = "https://drive.google.com/u/0/uc?id=1qbgfDLpn4FSy165Gcgg2r7iHnmSKtPFK&export=download"
        self.spliter = 1
        self.neuralNetwork = MLPClassifier()
        self.accuracy = 0
        self.dataset = []
        return {"status": "OK"}

    def load_dataset(self):
        self.init()
        self.dataset = Dataset().get_dataset(self.url, self.spliter)
        return {"dataset": self.dataset}

    def training(self):
        dataset = load_wine()
        x_train, x_test, y_train, y_test = train_test_split(dataset.data, dataset.target, test_size=0.20, random_state=4)
        NN = self.neural
        NN.fit(x_train, y_train)
        y_pred = NN.predict(x_test)
        self.accuracy = accuracy_score(y_test,y_pred)*100
        json = {"accuracy": self.accuracy}
        return json

    def get_accuracy(self):
        json = {"accuracy": self.accuracy}
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