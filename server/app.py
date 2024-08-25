# server/app.py
#!/usr/bin/env python3

from flask import Flask, make_response
from flask_migrate import Migrate

from models import db, Earthquake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


@app.route('/')
def index():
    body = {'message': 'Flask SQLAlchemy Lab 1'}
    return make_response(body, 200)

# Add views here
@app.route('/earthquakes/<int:id>')
def quake_by_id(id):
    earthquake = Earthquake.query.filter_by(id=id).first()
    if earthquake:
        return make_response(earthquake.to_dict(), 200)
    else:
        return make_response({"message": "Earthquake 9999 not found."}, 404)
    
@app.route('/earthquakes/magnitude/<float:mag>')
def quake_mags(mag):
    earthquakes = Earthquake.query.filter(Earthquake.magnitude >= mag).all()
    earthquake_list= []
    for earthquake in earthquakes:
        earthquake_list.append(earthquake.to_dict())
    body = {
        'count': len(earthquake_list),
        'quakes': earthquake_list
    }
    return make_response(body, 200)


if __name__ == '__main__':
    app.run(port=5555, debug=True)
