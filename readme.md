# API Documentation
[docs/api_docs.md](docs/api_docs.md)

# Running this repo

1. cd into the root of this repository
2. Type `python -m virtualenv venv` (you may need to use `python3` to ensure the right version)
3. Type `npm install -g api-spec-converter`
4. For macOS/Linux, type `source venv/bin/activate`. For Windows, type `.\env\Scripts\activate`
5. Type `pip install -r requirements.txt`
6. (Only need to do this once) `chmod +x dev_flask.sh`
7. `./dev_flask.sh` to start the app. You may query endpoints at `localhost:5000`

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
