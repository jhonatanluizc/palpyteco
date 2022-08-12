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