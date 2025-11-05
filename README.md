
# Flask Camping Fun API

A Flask API for managing campers, activities, and signups.

## Setup

1. Clone the repository
2. Create virtual environment: `python -m venv env`
3. Activate environment: `source env/bin/activate` (Mac/Linux) or `.\env\Scripts\activate` (Windows)
4. Install dependencies: `pip install -r requirements.txt`
5. Run migrations: `cd server && flask db upgrade head`
6. Start server: `python server/app.py`

## API Endpoints

- GET `/campers` - List all campers
- POST `/campers` - Create a new camper
- GET `/campers/<id>` - Get camper details
- PATCH `/campers/<id>` - Update camper
- GET `/activities` - List all activities  
- DELETE `/activities/<id>` - Delete activity
- POST `/signups` - Create a signup
