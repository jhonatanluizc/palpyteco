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
flask --app main --debug run --no-debugger --no-reload
flask --app main --debug run --no-debugger --reload
```

## Upload Heroku
### Include a Procfile that specifies the commands
```
web: gunicorn main:app
```
### Generate Requirements
```
python -m pip freeze > requirements.txt
```

### Dependencies
```
python -m pip install requests
python -m pip install -U scikit-learn
python -m pip install gunicorn
python -m pip install beautifulsoup4
python -m pip install html5lib
python -m pip install lxml
```