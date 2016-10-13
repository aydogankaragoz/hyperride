# -*- coding: utf-8 -*-
import os
from flask import Flask, render_template, request, g, jsonify
from sqlalchemy.orm import sessionmaker
import requests
import json
import model
import telegram
from raven.contrib.flask import Sentry
from rq import Queue
from worker import conn
app = Flask(__name__)
sentry = Sentry(app, dsn=os.environ['SENTRY_DSN'])
q = Queue(connection=conn)


def get_session():
    # session is stored in application global
    if not hasattr(g, 'session'):
        engine = model.connect_db()
        Session = sessionmaker(bind=engine)
        g.session = Session()
    return g.session


@app.route("/")
def hello():
    return render_template('index.html')


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
    sex = response['athlete']['sex']
    email = response['athlete']['email']

    # Registering
    session = get_session()

    if session.query(model.Athlete).get(id):
        telegram.existingUser(firstname, lastname)
        return render_template('existing_user.html',
                               firstname=firstname,
                               profile=profile,
                               email=email)
    else:
        new_athlete = model.Athlete(id,
                                    access_token,
                                    firstname,
                                    lastname,
                                    profile_medium,
                                    profile,
                                    sex,
                                    email)
        session.add(new_athlete)
        session.commit()
        telegram.newUser(firstname, lastname)
        return render_template('new_user.html',
                               firstname=firstname,
                               profile=profile,
                               email=email)


@app.route("/webhook", methods=['POST'])
def webHook():
    requestDict = json.loads(request.data)

    owner_id = requestDict["owner_id"]
    activity_id = requestDict["object_id"]

    from generators import analyse_activity

    q.enqueue(analyse_activity, owner_id, activity_id)

    return 'OK'


if __name__ == "__main__":
    app.run(debug=True)
