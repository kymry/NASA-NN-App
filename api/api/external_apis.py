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
'''

import requests
import json
from collections import OrderedDict
from .sql_models import Sol, Flare
import datetime
from dateutil import parser

API_KEY = "p5G79FjyWMrq7DiKGKNb0XEsc49ROtPjvSSbJigx"


def get_solarflare_data(db):
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
        pass
        #raise ConnectionError


def update_sqldb_flare_date(db, data):
    for elem in data:
        flare = Flare(id=elem['flrID'])
        try: flare.begin_time = elem['beginTime']
        except: pass
        try: flare.peak_time = parser.isoparse(elem['peakTime'])
        except: pass
        try: flare.end_time = parser.isoparse(elem['endTime'])
        except: pass
        try: flare.pressure = parser.isoparse(elem['classType'])
        except: pass
        try: flare.activity_region = elem['activeRegionNum']
        except: pass

        # add unique entries only
        if not db.session.query(Flare).filter(Flare.id == elem["flrID"]):
            db.session.add(flare)
            db.session.commit()


def get_mars_weather_data(mongodb, sqldb):
    """ Queries the NASA mars weather API """
    endpoint = "https://api.nasa.gov/insight_weather/?api_key=" + API_KEY + "&feedtype=json&ver=1.0"
    raw_output = requests.get(endpoint)

    if raw_output.ok:
        sols = json.loads(raw_output.content, object_pairs_hook=OrderedDict)
        update_sqldb_mars_data(sqldb, sols)
        update_mongoddb_mars_data(mongodb, sols)
    else:
        raise ConnectionError


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



