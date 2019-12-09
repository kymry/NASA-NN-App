''' Retrieve daily data from NASA http APIs
    NASA API Key: p5G79FjyWMrq7DiKGKNb0XEsc49ROtPjvSSbJigx
    NAS URL: https://api.nasa.gov/

    ----   Mars Weather Data API   ----
    https://mars.nasa.gov/insight/weather/
    GET https: //api.nasa.gov/insight_weather/?api_key=DEMO_KEY&feedtype=json&ver=1.0
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


def get_mars_data():
    ''' Queries the NASA mars weather API '''
    pass







