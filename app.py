from flask import Flask, render_template, request
import os
import requests
app = Flask(__name__)


@app.route("/")
def hello():
    return render_template('hello.html')


@app.route("/token_exchange")
def token_exchange():
    state = request.args.get('state', '')
    code = request.args.get('code', '')

    payload = {'client_id': os.environ['CLIENT_ID'],
               'client_secret': os.environ['CLIENT_SECRET'],
               'code': code}

    r = requests.post('https://www.strava.com/oauth/token', data=payload)
    return r.text

if __name__ == "__main__":
    app.run()
