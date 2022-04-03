import requests

BASE_URL = "https://api.edamam.com/api/recipes/v2"
APP_KEY = "6a51ffd51278380abcfcc9067cbacb1f"
APP_Id = "2707c6f4"

params = {
    "type": "public",
    "q": "chicken",
    "app_id": APP_Id,
    "app_key": APP_KEY,
}

response = requests.get(BASE_URL, params=params).json()

print(response)
