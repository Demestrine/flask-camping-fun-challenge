from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy.orm import validates

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Models
class Camper(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    signups = db.relationship('Signup', backref='camper', cascade='all, delete-orphan')
    
    @validates('name')
    def validate_name(self, key, name):
        if not name:
            raise ValueError("Name is required")
        return name
    
    @validates('age')
    def validate_age(self, key, age):
        age = int(age)
        if not (8 <= age <= 18):
            raise ValueError("Age must be between 8 and 18")
        return age

class Activity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    difficulty = db.Column(db.Integer, nullable=False)
    signups = db.relationship('Signup', backref='activity', cascade='all, delete-orphan')

class Signup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.Integer, nullable=False)
    camper_id = db.Column(db.Integer, db.ForeignKey('camper.id'), nullable=False)
    activity_id = db.Column(db.Integer, db.ForeignKey('activity.id'), nullable=False)
    
    @validates('time')
    def validate_time(self, key, time):
        time = int(time)
        if not (0 <= time <= 23):
            raise ValueError("Time must be between 0 and 23")
        return time

# Routes
@app.route('/campers', methods=['GET'])
def get_campers():
    campers = Camper.query.all()
    return jsonify([{'id': c.id, 'name': c.name, 'age': c.age} for c in campers])

@app.route('/campers/<int:id>', methods=['GET'])
def get_camper(id):
    camper = Camper.query.get(id)
    if not camper:
        return jsonify({'error': 'Camper not found'}), 404
    
    return jsonify({
        'id': camper.id,
        'name': camper.name,
        'age': camper.age,
        'signups': [{
            'id': s.id,
            'time': s.time,
            'activity_id': s.activity_id,
            'camper_id': s.camper_id,
            'activity': {
                'id': s.activity.id,
                'name': s.activity.name,
                'difficulty': s.activity.difficulty
            }
        } for s in camper.signups]
    })

@app.route('/campers', methods=['POST'])
def create_camper():
    try:
        data = request.get_json()
        camper = Camper(name=data['name'], age=data['age'])
        db.session.add(camper)
        db.session.commit()
        return jsonify({'id': camper.id, 'name': camper.name, 'age': camper.age}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'errors': [str(e)]}), 400

@app.route('/campers/<int:id>', methods=['PATCH'])
def update_camper(id):
    camper = Camper.query.get(id)
    if not camper:
        return jsonify({'error': 'Camper not found'}), 404
    
    try:
        data = request.get_json()
        if 'name' in data:
            camper.name = data['name']
        if 'age' in data:
            camper.age = data['age']
        
        db.session.commit()
        return jsonify({'id': camper.id, 'name': camper.name, 'age': camper.age}), 202
    except Exception as e:
        db.session.rollback()
        return jsonify({'errors': [str(e)]}), 400

@app.route('/activities', methods=['GET'])
def get_activities():
    activities = Activity.query.all()
    return jsonify([{'id': a.id, 'name': a.name, 'difficulty': a.difficulty} for a in activities])

@app.route('/activities', methods=['POST'])
def create_activity():
    try:
        data = request.get_json()
        activity = Activity(name=data['name'], difficulty=data['difficulty'])
        db.session.add(activity)
        db.session.commit()
        return jsonify({'id': activity.id, 'name': activity.name, 'difficulty': activity.difficulty}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'errors': [str(e)]}), 400

@app.route('/activities/<int:id>', methods=['DELETE'])
def delete_activity(id):
    activity = Activity.query.get(id)
    if not activity:
        return jsonify({'error': 'Activity not found'}), 404
    
    db.session.delete(activity)
    db.session.commit()
    return '', 204

@app.route('/signups', methods=['POST'])
def create_signup():
    try:
        data = request.get_json()
        signup = Signup(
            time=data['time'],
            camper_id=data['camper_id'],
            activity_id=data['activity_id']
        )
        db.session.add(signup)
        db.session.commit()
        
        camper = Camper.query.get(signup.camper_id)
        activity = Activity.query.get(signup.activity_id)
        
        return jsonify({
            'id': signup.id,
            'time': signup.time,
            'camper_id': signup.camper_id,
            'activity_id': signup.activity_id,
            'camper': {'id': camper.id, 'name': camper.name, 'age': camper.age},
            'activity': {'id': activity.id, 'name': activity.name, 'difficulty': activity.difficulty}
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'errors': [str(e)]}), 400

if __name__ == '__main__':
    app.run(port=5555, debug=True)