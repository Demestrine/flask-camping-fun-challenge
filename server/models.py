from . import db
from sqlalchemy.orm import validates

class Camper(db.Model):
    __tablename__ = 'campers'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    
    # a camper can have many signups
    signups = db.relationship('Signup', back_populates='camper', cascade='all, delete-orphan')
    
    @validates('name')
    def validate_name(self, key, name):
        # name can't be empty
        if not name:
            raise ValueError("Name is required")
        return name
    
    @validates('age')
    def validate_age(self, key, age):
        # age must be between 8 and 18
        age = int(age)
        if not (8 <= age <= 18):
            raise ValueError("Age must be between 8 and 18")
        return age
    
    def to_dict(self, include_signups=False):
        data = {
            'id': self.id,
            'name': self.name,
            'age': self.age
        }
        # include signups if requested
        if include_signups:
            data['signups'] = [signup.to_dict() for signup in self.signups]
        return data

class Activity(db.Model):
    __tablename__ = 'activities'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    difficulty = db.Column(db.Integer, nullable=False)
    
    # an activity can have many signups
    signups = db.relationship('Signup', back_populates='activity', cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'difficulty': self.difficulty
        }

class Signup(db.Model):
    __tablename__ = 'signups'
    
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.Integer, nullable=False)
    
    # link to camper and activity
    camper_id = db.Column(db.Integer, db.ForeignKey('campers.id'), nullable=False)
    activity_id = db.Column(db.Integer, db.ForeignKey('activities.id'), nullable=False)
    
    # relationships to connect camper and activity
    camper = db.relationship('Camper', back_populates='signups')
    activity = db.relationship('Activity', back_populates='signups')
    
    @validates('time')
    def validate_time(self, key, time):
        # time must be between 0 and 23 (24-hour format)
        time = int(time)
        if not (0 <= time <= 23):
            raise ValueError("Time must be between 0 and 23")
        return time
    
    @validates('camper_id')
    def validate_camper(self, key, camper_id):
        # make sure the camper exists
        from server import db
        if not db.session.get(Camper, camper_id):
            raise ValueError("Camper not found")
        return camper_id
    
    @validates('activity_id')
    def validate_activity(self, key, activity_id):
        # make sure the activity exists
        from server import db
        if not db.session.get(Activity, activity_id):
            raise ValueError("Activity not found")
        return activity_id
    
    def to_dict(self):
        return {
            'id': self.id,
            'time': self.time,
            'camper_id': self.camper_id,
            'activity_id': self.activity_id,
            'camper': self.camper.to_dict(),
            'activity': self.activity.to_dict()
        }