import model
import telegram
from sqlalchemy.orm import sessionmaker

engine = model.connect_db()
Session = sessionmaker(bind=engine)
session = Session()

def analyse_activity(owner_id, activity_id):
    athlete = session.query(model.Athlete).get(owner_id)

    telegram.newActivity(athlete.firstname, athlete.lastname, activity_id)
