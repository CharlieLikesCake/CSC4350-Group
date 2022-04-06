import requests
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

BASE_URL = "https://api.edamam.com/api/recipes/v2"

# function returns a list of 20(?) random dishes according to a query (q)
def getRandomRecipeList(q):
    params = {
        "type": "public",
        "app_id": os.getenv("APP_ID"),
        "app_key": os.getenv("APP_KEY"),
        "q": q,
        "random": True,
    }

    response = requests.get(BASE_URL, params=params).json()["hits"]

    randomRecipeList = []

    for hit in response:
        randomRecipeList.append(
            {
                "label": hit["recipe"]["label"],
                "image": hit["recipe"]["image"],
                "source": hit["recipe"]["source"],
                "url": hit["recipe"]["url"],
            }
        )

    return randomRecipeList
