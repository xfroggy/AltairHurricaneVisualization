from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
from sqlalchemy.types import Integer, Text, String, DateTime, Float
from os import environ
from sqlalchemy import create_engine

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://hurricane:hurricane_pw@localhost:8889/hurricane'
app.config['SQLALCHEMY_ECHO'] = True
engine = create_engine('mysql+pymysql://hurricane:hurricane_pw@localhost:8889/hurricane', echo=True)

db = SQLAlchemy(app)

# for intial db construction
class Hurricane(db.Model):
    id = db.Column(db.Integer, primary_key =True)
    identifier = db.Column(db.String(20))
    name = db.Column(db.String(50))
    num_pts = db.Column(db.Integer)
    datetime = db.Column(db.DateTime)
    record_id = db.Column(db.String(10))
    status = db.Column(db.String(5))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    max_wind = db.Column(db.Float)
    min_pressure = db.Column(db.Float)
    ne34ktr = db.Column(db.Float)
    se34ktr = db.Column(db.Float)
    sw34ktr = db.Column(db.Float)
    nw34ktr = db.Column(db.Float)
    ne50ktr = db.Column(db.Float)
    se50ktr = db.Column(db.Float)
    sw50ktr = db.Column(db.Float)
    nw50ktr = db.Column(db.Float)
    ne64ktr = db.Column(db.Float)
    se64ktr = db.Column(db.Float)
    sw64ktr = db.Column(db.Float)
    nw64ktr = db.Column(db.Float)

# adds pandas DataFrame data to the database, replacing old with new data
def update_database(hurricane_data):
    hurricane_data.to_sql(
        "hurricane",
        con = engine,
        if_exists='replace',
        index = False,
        dtype= {
            "identifier": String(20),
            "name": String(50,),
            "num_pts": Integer,
            "datetime": DateTime,
            "record_id": String(10),
            "status": String(5),
            "latitude": Float,
            "longitude": Float,
            "max_wind": Float,
            "min_pressure": Float,
            "ne34ktr": Float,
            "se34ktr": Float,
            "sw34ktr": Float,
            "nw34ktr": Float,
            "ne50ktr": Float,
            "se50ktr": Float,
            "sw50ktr": Float,
            "nw50ktr": Float,
            "ne64ktr": Float,
            "se64ktr": Float,
            "sw64ktr": Float,
            "nw64ktr": Float
        }
    )