import model
import telegram


def analyse_activity(session, owner_id, activity_id):
    athlete = session.query(model.Athlete).get(owner_id)

    telegram.newActivity(athlete.firstname, athlete.lastname, activity_id)
