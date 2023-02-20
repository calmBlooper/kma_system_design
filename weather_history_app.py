import datetime as dt

import json




import requests

from flask import Flask, jsonify, request





API_TOKEN = "" 

WEATHER_API_KEY = ""




app = Flask(__name__)







def get_weather(location: str,date: str):

    url_base_url = "http://api.weatherapi.com/v1/history.json"

    url = f"{url_base_url}?key={WEATHER_API_KEY}&q={location}&dt={date}" 

    response = requests.request("GET", url, headers={}, data={})

    return json.loads(response.text)







class InvalidUsage(Exception):

    status_code = 400




    def __init__(self, message, status_code=None, payload=None):

        Exception.__init__(self)

        self.message = message

        if status_code is not None:

            self.status_code = status_code

        self.payload = payload




    def to_dict(self):

        rv = dict(self.payload or ())

        rv["message"] = self.message

        return rv







@app.errorhandler(InvalidUsage)

def handle_invalid_usage(error):

    response = jsonify(error.to_dict())

    response.status_code = error.status_code

    return response







@app.route("/")

def home_page():

    return "<p><h2>KMA L2: Python Saas with weather from Voldemar.</h2></p>"







@app.route(

    "/api/v1/weather",

    methods=["GET"],

) 

def weather_endpoint():

    start_dt = dt.datetime.now()

    json_data = request.get_json()




    if json_data.get("token") is None:

        raise InvalidUsage("token is required", status_code=400)

    if json_data.get("requester_name") is None:

        raise InvalidUsage("Requester name is required", status_code=400)

    if json_data.get("location") is None:

        raise InvalidUsage("Location name is required", status_code=400)

    if json_data.get("date") is None:

        raise InvalidUsage("Weather date is required", status_code=400)




    token = json_data.get("token")
    requester_name=json_data.get("requester_name")
    location=json_data.get("location")
    date=json_data.get("date")



    if token != API_TOKEN:

        raise InvalidUsage("wrong API token", status_code=403)




    formed_request = get_weather(location,date)




    end_dt = dt.datetime.now()
 




    result = { 
        "requester_name": requester_name,
        "timestamp": end_dt.isoformat(), 
        "location": location,
        "weather":     formed_request 
    }




    return result
