from flask import Flask
from api.controllers.neural_network import NeuralNetwork
from api.controllers.dataset import Dataset

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "hello"

@app.route("/hello")
def teste():
    from flask import render_template
    return render_template("hello.html")

@app.get('/api')
def teste_api():
    return NeuralNetwork().test_training()

@app.get('/dataset')
def get_dataset():
    url = "https://drive.google.com/u/0/uc?id=1qbgfDLpn4FSy165Gcgg2r7iHnmSKtPFK&export=download"
    return {"dataset": Dataset().get_dataset(url)}