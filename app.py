import os
from flask import Flask, render_template, request
import requests
app = Flask(__name__)


@app.route("/")
def hello():
    return render_template('hello.html')


@app.route("/token_exchange")
def token_exchange():
    code = request.args.get('code', '')

    payload = {'client_id': os.environ['CLIENT_ID'],
               'client_secret': os.environ['CLIENT_SECRET'],
               'code': code}

    r = requests.post('https://www.strava.com/oauth/token', data=payload)
    response = r.json()

    id = response['athlete']['id']
    access_token = response['access_token']

    username = response['athlete']['username']
    firstname = response['athlete']['firstname']
    lastname = response['athlete']['lastname']
    
    profile_medium = response['athlete']['profile_medium']
    profile = response['athlete']['profile']
    
    city = response['athlete']['city']
    state = response['athlete']['state']
    country = response['athlete']['country']
    
    sex = response['athlete']['sex']
    email = response['athlete']['email']

    created_at = response['athlete']['created_at']
    updated_at = response['athlete']['updated_at']
    return profile + ' : ' + created_at 

if __name__ == "__main__":
    app.run()
