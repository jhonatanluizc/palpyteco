# palpyteco
#Análise de dados para palpites em apostas.

### Create an environment
```
mkdir myproject
cd myproject
py -3 -m venv venv
```

### Activate the environment
```
venv\Scripts\activate
```

### Install Flask
```
python.exe -m pip install --upgrade pip
pip install Flask
```

### Run the application
```
flask --app main run
```
or
```
flask --app main --debug run --no-debugger --no-reload
```

### Dependencies
```
python -m pip install requests
python -m pip install -U scikit-learn
```