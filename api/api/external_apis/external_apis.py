''' Retrieve data from NASA http APIs
    API Key: p5G79FjyWMrq7DiKGKNb0XEsc49ROtPjvSSbJigx
    URL: https://api.nasa.gov/

    ----   Mars Weather Data API   ----
    https://api.nasa.gov/assets/insight/InSight%20Weather%20API%20Documentation.pdf
    GET https://api.nasa.gov/insight_weather/?api_key=KEY&feedtype=json&ver=1.0
    returns: JSON

    ----   Space Weather Data API   ----
    https://ccmc.gsfc.nasa.gov/support/DONKI-webservices.php
    GET https://kauai.ccmc.gsfc.nasa.gov/DONKI/WS/get/FLR?startDate=yyyy-MM-dd&endDate=yyyy-MM-dd
    returns: JSON

    ---    Astronomy Picture of the Day ----
    GET https://api.nasa.gov/planetary/apod?api_key=KEY
    returns: JSON
'''

import requests
import urllib.request
import json
import os
from collections import OrderedDict
import datetime
from dateutil import parser
from ..models.apod import Apod
from ..models.flare import Flare
from ..models.sol import Sol


API_KEY = "p5G79FjyWMrq7DiKGKNb0XEsc49ROtPjvSSbJigx"
IMAGE_BASE_DIR = os.path.abspath(os.path.dirname(__file__))


def get_astronomy_pic_of_day(db):
    """ Queries the NASA Astronomy Picture of the Day (APOD) API """

    endpoint = 'https://api.nasa.gov/planetary/apod?api_key=' + API_KEY
    raw_data = requests.get(endpoint)

    if raw_data.ok and raw_data.content:
        output = json.loads(raw_data.content)
        process_astronomy_pic_of_day(db, output)
    else:
        print('Conection Error')


def process_astronomy_pic_of_day(db, data):
    apod = Apod(date=parser.parse(data['date'], yearfirst=True))
    if 'explanation' in data: apod.explanation = data['explanation']
    if 'media_type' in data: apod.media_type = data['media_type']
    if 'title' in data: apod.title = data['title']
    if 'url' in data: apod.url = data['url']

    file_system_path = os.path.join(IMAGE_BASE_DIR, 'images/daily', data['date'] + '.jpg')
    apod.path = file_system_path

    print(parser.parse(data['date'], yearfirst=True))
    # add unique entries only
    if not db.session.query(Apod).filter(Apod.date == parser.parse(data['date'], yearfirst=True)):
        db.session.add(apod)
        db.session.commit()
        urllib.request.urlretrieve(data['url'], file_system_path)
        print(apod)


def get_solar_flare(db):
    ''' Queries the NASA solar flare API '''
    start_date = str(datetime.date(2017, 2, 2))
    end_date = str(datetime.date(2019, 2, 3))
    endpoint = 'https://kauai.ccmc.gsfc.nasa.gov/DONKI/WS/get/FLR?startDate=' + start_date + '&endDate=' + end_date
    raw_data = requests.get(endpoint)

    # API was successfully queried
    if raw_data.ok and raw_data.content:
        output = json.loads(raw_data.content)
        update_sqldb_flare_date(db, output)
    else:
        print('ConnectionError')


def update_sqldb_flare_date(db, data):
    for elem in data:
        flare = Flare(id=elem['flrID'])
        try: flare.begin_time = parser.parse(elem['beginTime'])
        except: pass
        try: flare.peak_time = parser.parse(elem['peakTime'])
        except: pass
        try: flare.end_time = parser.parse(elem['endTime'])
        except: pass
        try: flare.class_type = str(elem['classType'])
        except: pass
        try: flare.activity_region = str(elem['activeRegionNum'])
        except: pass

        # add unique entries only
        if not db.session.query(Flare).filter(Flare.id == elem["flrID"]):
            db.session.add(flare)
            db.session.commit()


def get_mars_weather(mongodb, sqldb):
    """ Queries the NASA mars weather API """
    endpoint = "https://api.nasa.gov/insight_weather/?api_key=" + API_KEY + "&feedtype=json&ver=1.0"
    raw_output = requests.get(endpoint)

    if raw_output.ok:
        sols = json.loads(raw_output.content, object_pairs_hook=OrderedDict)
        update_sqldb_mars_data(sqldb, sols)
        update_mongoddb_mars_data(mongodb, sols)
    else:
        print('ConnectionError')


def update_mongoddb_mars_data(db, sols):
    for sol in sols["sol_keys"]:
        sol_object = sols[sol]
        sol_object['sol'] = sol
        sol_object['_id'] = sol
        sol_object.move_to_end('sol', last=False)
        db.db['solweather'].update({'_id': sol}, sol_object, upsert=True)


def update_sqldb_mars_data(db, sols):
    for sol in sols["sol_keys"]:
        current_sol = sols[sol]
        sol_object = Sol(sol=int(sol))
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

        # add unique entries only
        if not db.session.query(Sol).filter(Sol.sol == int(sol)):
            db.session.add(sol_object)
            db.session.commit()



