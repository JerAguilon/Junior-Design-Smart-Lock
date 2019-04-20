# What is this?

![](https://camo.githubusercontent.com/19b06d2af4f1078cd401fbf66d6eff38fbe650fd/68747470733a2f2f692e696d6775722e636f6d2f6c4c34724577782e706e67)

This is the backend service for a smart box device for Georgia Tech's junior design course. It allows for users to unlock a lock, view history of actions to a lock, update passwords, and manage lock metadata in one compact service. See [here](https://github.com/myothiha09/SmartBox) for complete project documentation as well as frontend client code.

# API Documentation
[docs/api_docs.md](docs/api_docs.md)

# Running this repo

### Prerequisites

You will need to configure an `env/variables.ini` file that contains all the environment variables needed to get the server to run. It should follow the format in `env/variables.ini.example`. H

In total, you should create _3_ [Firebase instances](https://console.firebase.google.com/u/0/): one for development, one for testing, and one for production. Once this is done, for each firebase instance:

1. Download the Firebase JSON key by following the "Initialize the SDK" instructions provided by Google Firebase [here](https://firebase.google.com/docs/admin/setup).
2. Update the serviceAccount variable for dev, test, and prod to be the location of the firebase key.
3. Get the apiKey, authDomain, databaseURL, and storageBucket from the firebase console. The easiest way to look these up is:
    a) Go to the project overview page in the Firebase console
    b) Click the `+` in the top bar
    c) Click the </> button to add a web app.
    d) Simply copy and paste the variables that pop up. You do not need to create a web app.

### Linux/MacOS

1. cd into the root of this repository
2. Type `python -m virtualenv venv` (you may need to use `python3` to ensure the right version)
3. Type `npm install -g api-spec-converter`
4. For macOS/Linux, type `source venv/bin/activate`.
5. Type `pip install -r requirements.txt`
6. (Only need to do this once) `chmod +x dev_flask.sh`
7. `./dev_flask.sh` to start the app. You may query endpoints at `localhost:5000`

### Windows

**Warning: these instructions are lightly tested only due to no backend coders using Windows.
  UNIX operating systems are the preferred platform for this server.**

1. cd into the root of this repository
2. Type `python -m virtualenv venv` (you may need to use `python3` to ensure the right version)
3. Type `npm install -g api-spec-converter`
4. For Windows, type `.\venv\Scripts\activate`
5. Type `pip install -r requirements.txt`
6. On command prompt: `C:\path\to\app>set FLASK_APP=run.py`
7. Type `flask run` or `python -m flask run`

# Playing with the endpoints

This package has great tool to play with the API. Simply go to `localhost:5000/docs`
to fiddle with endpoints. Copy/paste your OAuth key into the API key field to validate requests.

# Updating the API docs

1. If you don't have swagger-markdown and api-spec converter, install them. `npm install swagger-markdown api-spec-converter`
2. From the root directory of the project, run `python create_docs.py`

# Running tests

`chmod +x run_tests.sh` if you haven't already.

`./run_tests.sh`

# How can I ping my localhost server from an external device?

I recommend [ngrok](https://ngrok.com/), which creates a secure URL
to the server. Once ngrok has been installed, start the flask server
and type `/path/to/ngrok http 5000` to generate a URL.

# Troubleshooting

1. `dev_flask.sh` is not working: likely this is due to odd setups on your system. You can try running `export FLASK_APP=run.py && python -m flask run` in the root of this project.
1. It runs but immediately crashes: most likely, this is due to environment setup issues. Double check that your `env/variables.ini` is correctly configured.

