# underScore
![Python App CI](https://github.com/exmaple/underScore/workflows/Python%20App%20CI/badge.svg)

Is a news discord bot that reports the scores of your favourite teams.

# Development
We are using [python 3.8](https://www.python.org/downloads/) in a virtual environment for development.

### Environment Setup
Setting up python:
```
$ python3 -m venv venv
$ source venv/bin/activate
(venv)$ python --version
Python 3.8.1
```

Set the environment token:
```
$ export TOKEN=[bot-token]
```

### Installing Requirements
```
(venv)$ pip install -r requirements.txt
```

### Running the Bot
```
(venv)$ python bot.py
```
Alternatively you can run the bot with the `--token` flag and give it a token other than the one set in your environment.

### Tests
```
(venv)$ pip install -r test_requirements.txt
(venv)$ pytest -v tests/
```
