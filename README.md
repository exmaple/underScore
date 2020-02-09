# underScore

Is a news discord bot that reports the scores of your favourite teams.

# Development
We are using [python 3.8](https://www.python.org/downloads/) in a virtual environment for development.

### Environment Setup
```
$ python3 -m venv venv
$ source venv/bin/activate
(venv)$ python --version
Python 3.8.1
```

### Installing Requirements
```
(venv)$ pip install -r requirements.txt
```

### Running the Bot
```
(venv)$ python bot.py --token [bot-token]
```

#### Troubleshooting
Any errors with solutions encountered during development can be documented here.

##### "Cannot connect to host discordapp.com:443"
To solve (on macOS) navigate to `/Applications/Python\ 3.8` and run the "Install Certificates.command" file.  This will run a shell script the pip installs a package that will give your machine the credentials needed to run the bot. 
