from asyncio.windows_events import NULL
from sklearn.datasets import load_wine
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import confusion_matrix, accuracy_score
from api.controllers.dataset import Dataset


class NeuralNetwork():

    neural_network = NULL
    accuracy = NULL 
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


      