import requests
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

BASE_URL = "https://api.edamam.com/api/recipes/v2"

params = {
    "type": "public",
    "q": "chicken",
    "app_id": os.getenv("APP_ID"),
    "app_key": os.getenv("APP_KEY"),
}

response = requests.get(BASE_URL, params=params).json()

print(response)
