''' ----   Mars Weather Data API (mars_api)  ----
    Documentation: https://application.nasa.gov/assets/insight/InSight%20Weather%20API%20Documentation.pdf
    GET https://application.nasa.gov/insight_weather/?api_key=KEY&feedtype=json&ver=1.0
    returns: JSON

    ----   Solar Flare Data API (flare_api)   ----
    Documentation: https://ccmc.gsfc.nasa.gov/support/DONKI-webservices.php
    GET https://kauai.ccmc.gsfc.nasa.gov/DONKI/WS/get/FLR?startDate=yyyy-MM-dd&endDate=yyyy-MM-dd
    returns: JSON

    ----   API: Astronomy Picture of the Day (apod_api)   ----
    Documentation: https://apod.nasa.gov/apod/astropix.html
    GET https://application.nasa.gov/planetary/apod?api_key=KEY
    returns: JSON
'''
import requests
import urllib.request
import json
import os
from collections import OrderedDict
import datetime
from dateutil import parser
from models.models import Apod, Flare, Sol


API_KEY = "nnbXgYgvAzynrP8e3KVd9WgPsfIl0eHweH2ZQSsu"
IMAGE_BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


def query_apis(app, mongodb, sqldb):
    """ Driver function that queries all external APIs.
        Which APIs are called daily is controlled from here """
    with app.app_context():
        query_apod_api(sqldb)
        query_flare_api(sqldb)
        query_mars_api(mongodb, sqldb)


def query_apod_api(db):
    endpoint = 'https://api.nasa.gov/planetary/apod?api_key=' + API_KEY
    raw_data = requests.get(endpoint)

    if raw_data.ok and raw_data.content:
        output = json.loads(raw_data.content)
        process_apod_api(db, output)


def process_apod_api(db, data):
    apod = Apod()
    apod.path = os.path.join(IMAGE_BASE_DIR, 'images/daily', data['date'] + '.jpg')

    # check for missing columns
    for field in Apod.__table__.columns.keys():
        if field in data:
            setattr(apod, field, data[field])

    # check for duplicates
    if not db.session.query(Apod).filter(Apod.date == data['date']).scalar():
        db.session.add(apod)
        db.session.commit()
        urllib.request.urlretrieve(data['url'], apod.path)


def query_flare_api(db):
    start_date = str(datetime.date.today())
    end_date = str(datetime.date.today())
    endpoint = 'https://kauai.ccmc.gsfc.nasa.gov/DONKI/WS/get/FLR?startDate=' + start_date + '&endDate=' + end_date
    raw_data = requests.get(endpoint)

    if raw_data.ok and raw_data.content:
        output = json.loads(raw_data.content)
        process_flare_api(db, output)


def process_flare_api(db, data):
    # check for missing values
    for elem in data:
        flare = Flare(id=elem['flrID'])
        if 'begin_time' in elem:
            flare.begin_time = parser.parse(elem['beginTime'])
        if 'peak_time' in elem:
            flare.peak_time = parser.parse(elem['peakTime'])
        if 'end_time' in elem:
            flare.end_time = parser.parse(elem['endTime'])
        if 'class_type' in elem:
            flare.class_type = str(elem['classType'])
        if 'activity_region' in elem:
            flare.activity_region = str(elem['activeRegionNum'])

        # check for duplicates
        if not db.session.query(Flare).filter(Flare.id == elem["flrID"]).scalar():
            db.session.add(flare)
            db.session.commit()
            print(elem)


def query_mars_api(mongodb, sqldb):
    endpoint = "https://api.nasa.gov/insight_weather/?api_key=" + API_KEY + "&feedtype=json&ver=1.0"
    raw_output = requests.get(endpoint)

    if raw_output.ok:
        sols = json.loads(raw_output.content, object_pairs_hook=OrderedDict)
        process_mars_api_sql(sqldb, sols)
        process_mars_api_mongo(mongodb, sols)


def process_mars_api_mongo(db, sols):
    for sol in sols["sol_keys"]:
        sol_object = sols[sol]
        sol_object['sol'] = sol
        sol_object['_id'] = sol
        sol_object.move_to_end('sol', last=False)
        db.db['solweather'].update({'_id': sol}, sol_object, upsert=True)


def process_mars_api_sql(db, sols):

    for sol in sols["sol_keys"]:
        current_sol = sols[sol]
        sol_object = Sol(sol=int(sol))
        # check for missing values
        try: sol_object.average_temperature = current_sol['AT']['av']
        except: pass
        try: sol_object.high_temperature = current_sol['AT']['mx']
        except: pass
        try: sol_object.horizontal_wind_speed = current_sol['HWS']['av']
        except: pass
        try: sol_object.low_temperature = current_sol['AT']['mn']
        except: pass
        try: sol_object.pressure = current_sol['PRE']['av']
        except: pass

        # check for duplicates
        if not db.session.query(Sol).filter(Sol.sol == int(sol)).scalar():
            db.session.add(sol_object)
            db.session.commit()
            print(sol)



