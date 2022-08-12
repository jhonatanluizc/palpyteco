from asyncio.windows_events import NULL
from sklearn.datasets import load_wine
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import confusion_matrix, accuracy_score
from api.controllers.dataset import Dataset
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
from datetime import date, datetime

class NeuralNetwork():

    neural_network = NULL
    accuracy = NULL 
    dataset = NULL
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
                "predict": response
            }

        return json
      