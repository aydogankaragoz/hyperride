import app
import model
import telegram


def analyse_activity(owner_id, activity_id):
    resp = requests.get(url)
    return len(resp.text.split())

    session = app.get_session()
    athlete = session.query(model.Athlete).get(owner_id)

    telegram.newActivity(athlete.firstname, athlete.lastname, activity_id)
