import flask
import requests
import json


app = flask.Flask(__name__)

BASE_URL = "https://api.edamam.com/api/recipes/v2"
APP_KEY = "6a51ffd51278380abcfcc9067cbacb1f"
APP_Id = "2707c6f4"

params = {
    "app_key": APP_KEY,
    "app_id": APP_Id,
    "q": "chicken",
}

response = requests.get(BASE_URL, params=params)
response_json = response.json()["recipe"]

print(response_json)
