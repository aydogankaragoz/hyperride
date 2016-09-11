import os
from flask import Flask, render_template, request
import requests
import model
app = Flask(__name__)

def get_session():
    # session is stored in application global
    if not hasattr(g, 'session'):
        engine = model.connect_db()
        Session = sessionmaker(bind=engine)
        g.session = Session()
    return g.session


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
    
    # Parsing the Response
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

    # Registering
    session = get_session()
    new_athlete = model.Athlete(id, access_token, username,
    	firstname, lastname, profile_medium, profile,
    	city, state, country, sex, email)
    session.add(new_athlete)
    session.commit()
    return "Registered: " + firstname 

if __name__ == "__main__":
    app.run(debug=True)
