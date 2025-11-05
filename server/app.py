from flask import Flask, request, jsonify
from server import db, create_app
from models import Camper, Activity, Signup

app = create_app()

# handle validation errors gracefully
@app.errorhandler(ValueError)
def handle_validation_error(e):
    return jsonify({'errors': [str(e)]}), 400

# get all campers
@app.route('/campers', methods=['GET'])
def get_campers():
    campers = Camper.query.all()
    return jsonify([camper.to_dict() for camper in campers]), 200

# get a specific camper by id
@app.route('/campers/<int:id>', methods=['GET'])
def get_camper(id):
    camper = db.session.get(Camper, id)
    if not camper:
        return jsonify({'error': 'Camper not found'}), 404
    return jsonify(camper.to_dict(include_signups=True)), 200

# create a new camper
@app.route('/campers', methods=['POST'])
def create_camper():
    try:
        data = request.get_json()
        camper = Camper(
            name=data['name'],
            age=data['age']
        )
        db.session.add(camper)
        db.session.commit()
        return jsonify(camper.to_dict()), 201
    except ValueError as e:
        db.session.rollback()
        return jsonify({'errors': [str(e)]}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'errors': ['Invalid data']}), 400

# update a camper's information
@app.route('/campers/<int:id>', methods=['PATCH'])
def update_camper(id):
    camper = db.session.get(Camper, id)
    if not camper:
        return jsonify({'error': 'Camper not found'}), 404
    
    try:
        data = request.get_json()
        if 'name' in data:
            camper.name = data['name']
        if 'age' in data:
            camper.age = data['age']
        
        db.session.commit()
        return jsonify(camper.to_dict()), 202
    except ValueError as e:
        db.session.rollback()
        return jsonify({'errors': [str(e)]}), 400

# get all activities
@app.route('/activities', methods=['GET'])
def get_activities():
    activities = Activity.query.all()
    return jsonify([activity.to_dict() for activity in activities]), 200

# delete an activity
@app.route('/activities/<int:id>', methods=['DELETE'])
def delete_activity(id):
    activity = db.session.get(Activity, id)
    if not activity:
        return jsonify({'error': 'Activity not found'}), 404
    
    db.session.delete(activity)
    db.session.commit()
    return '', 204

# create a new signup
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
        return jsonify(signup.to_dict()), 201
    except ValueError as e:
        db.session.rollback()
        return jsonify({'errors': [str(e)]}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'errors': ['Invalid data']}), 400

if __name__ == '__main__':
    app.run(port=5555, debug=True)