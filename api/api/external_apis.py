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


def get_mars_data(db, collection):
    """ Queries the NASA mars weather API for the following data and updates db

        -- Atmospheric temperature degrees celsius
        -- Horizontal wind speed, metres per second
        -- Atmospheric pressure, pascals

        db: MongoDB object
        collection: MongoDB collection """

    endpoint = "https://api.nasa.gov/insight_weather/?api_key=" + API_KEY + "&feedtype=json&ver=1.0"
    raw_output = requests.get(endpoint)

    if raw_output.ok:
        # object_pairs_hook is needed to maintain the ordering
        raw_output = json.loads(raw_output.content, object_pairs_hook=OrderedDict)
    else:
        pass
        # TODO raise exception and exit function

    # process sol JSON objects
    sols_data = []
    for sol in raw_output["sol_keys"]:
        sol_object = raw_output[sol]
        sol_object['sol'] = sol
        sol_object.move_to_end('sol', last=False)
        sols_data.append(raw_output[sol])

    db.db[collection].insert_many(sols_data)
