''' Retrieve daily data from NASA http APIs
    NASA API Key: p5G79FjyWMrq7DiKGKNb0XEsc49ROtPjvSSbJigx
    NAS URL: https://api.nasa.gov/

    ----   Mars Weather Data API   ----
    https://api.nasa.gov/assets/insight/InSight%20Weather%20API%20Documentation.pdf
    GET https://api.nasa.gov/insight_weather/?api_key=p5G79FjyWMrq7DiKGKNb0XEsc49ROtPjvSSbJigx&feedtype=json&ver=1.0
    returns: JSON

    ----   Space Weather Data API   ----
    https://ccmc.gsfc.nasa.gov/support/DONKI-webservices.php
    GET https://kauai.ccmc.gsfc.nasa.gov/DONKI/WS/get/FLR?startDate=yyyy-MM-dd&endDate=yyyy-MM-dd
    returns: JSON
    return format: flrID, instruments[(list of) displayName], beginTime, peakTime, endTime, classType, sourceLocation,
                   activeRegionNum, linkedEvents[(list of) activityID]
'''

import requests
import json
from collections import OrderedDict
from .sql_models import Sol

API_KEY = "p5G79FjyWMrq7DiKGKNb0XEsc49ROtPjvSSbJigx"


def get_solarflare_data(start_date, end_date):
    ''' Queries the NASA solar flare API '''

    endpoint = ('https://kauai.ccmc.gsfc.nasa.gov/DONKI/WS/get/FLR?startDate=' + start_date + '&endDate=' + end_date)
    data = requests.get(endpoint)
    output = None

    # API was successfully queried
    if data.ok:
        output = json.loads(data.content)

        # TODO: parse out needed data from output
        return output

    else:
        print("Can't access NASA solar flare API")


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
   #db.db['solweather'].update_many(sols, sols, upsert=True)


def update_sqldb_mars_data(db, sols):
    # each sol object is a dict
    # TODO: create function for try, excepts
    for x in sols["sol_keys"]:
        sol = sols[x]
        elem = Sol(sol=int(x))
        try:
            elem.average_temperature = sol['AT']['av']
        except KeyError:
            pass
        try:
            elem.high_temperature = sol['AT']['mx']
        except KeyError:
            pass
        try:
            elem.horizontal_wind_speed = sol['HWS']['av']
        except KeyError:
            pass
        try:
            elem.low_temperature = sol['AT']['mn']
        except KeyError:
            pass
        try:
            elem.pressure = sol['PRE']['av']
        except KeyError:
            pass
        if not db.session.query(Sol).filter(Sol.sol == int(x)):
            db.session.add(elem)
            db.session.commit()



