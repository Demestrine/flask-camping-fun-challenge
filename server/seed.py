import sys
import os

# Add the parent directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from server.app import app, db
from server.models import Camper, Activity, Signup

def seed_database():
    with app.app_context():
        # clear existing data
        db.drop_all()
        db.create_all()
        
        # create some campers
        campers = [
            Camper(name="Caitlin", age=8),
            Camper(name="Lizzie", age=9),
            Camper(name="Nicholas Martinez", age=12),
            Camper(name="Zoe", age=11)
        ]
        
        # create some activities
        activities = [
            Activity(name="Archery", difficulty=2),
            Activity(name="Swimming", difficulty=3),
            Activity(name="Hiking by the stream", difficulty=2),
            Activity(name="Listening to the birds chirp", difficulty=1),
            Activity(name="Canoeing", difficulty=3)
        ]
        
        # add to database
        db.session.add_all(campers)
        db.session.add_all(activities)
        db.session.commit()
        
        # create some signups
        signups = [
            Signup(camper_id=1, activity_id=1, time=10),
            Signup(camper_id=2, activity_id=2, time=14),
            Signup(camper_id=3, activity_id=3, time=8),
            Signup(camper_id=3, activity_id=4, time=13),
            Signup(camper_id=4, activity_id=5, time=16)
        ]
        
        db.session.add_all(signups)
        db.session.commit()
        
        print("database seeded successfully with sample data!")

if __name__ == '__main__':
    seed_database()