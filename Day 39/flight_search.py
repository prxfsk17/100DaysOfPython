import os
from dotenv import load_dotenv
import requests

class FlightSearch:
    #This class is responsible for talking to the Flight Search API.

    def __init__(self):
        load_dotenv()
        self.URL_IATA = os.getenv("URL_IATA")
        self.URL_TOKEN = os.getenv("URL_TOKEN")

    def get_iata(self, city_name):
        params = {
            "keyword": f"{city_name}",
            "max": 10,
            "include": "AIRPORTS"
        }
        head = {
            "Authorization": f"Bearer {self.get_token()}"
        }
        response = requests.get(url=self.URL_IATA, headers=head, params=params)
        response.raise_for_status()
        return response.json()["data"][0]["iataCode"]

    def get_token(self):
        head = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        data = {
            "grant_type": "client_credentials",
            "client_id": os.getenv("FLIGHT_API_KEY"),
            "client_secret": os.getenv("FLIGHT_API_SECRET")
        }
        response = requests.post(url=self.URL_TOKEN, headers=head, data=data)
        response.raise_for_status()
        return response.json()["access_token"]

