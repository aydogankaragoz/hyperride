import os
from flask import Flask, render_template, request, g
from sqlalchemy.orm import sessionmaker
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

    response = r.json()
    id = response['athlete']['id']
    access_token = response['access_token']
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

    if session.query(model.Athlete).get(id):
        return render_template('existing_user.html',
                               firstname=firstname,
                               profile=profile,
                               city=city,
                               state=state,
                               country=country,
                               email=email)
    else:
        new_athlete = model.Athlete(id,
                                    access_token,
                                    firstname,
                                    lastname,
                                    profile_medium,
                                    profile,
                                    city,
                                    state,
                                    country,
                                    sex,
                                    email)
        session.add(new_athlete)
        session.commit()
        return render_template('new_user.html',
                               firstname=firstname,
                               profile=profile,
                               city=city,
                               state=state,
                               country=country,
                               email=email)

if __name__ == "__main__":
    app.run(debug=True)
