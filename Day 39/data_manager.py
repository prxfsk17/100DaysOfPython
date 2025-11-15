import os
import requests
from dotenv import load_dotenv
from flight_search import FlightSearch

class DataManager:
    #This class is responsible for talking to the Google Sheet.

    def __init__(self, fs):
        load_dotenv()
        self.API_SHEET_URL_GET=os.getenv("API_SHEET_URL")
        self.API_SHEET_URL_PUT=self.API_SHEET_URL_GET+"/"
        self.API_SHEET_TOKEN=os.getenv("API_SHEET_TOKEN")
        self.HEADER={
            "Authorization" : os.getenv("API_SHEET_TOKEN")
        }
        self.flight_search=fs
        self.records = self.get_sheet()
        self.update_sheet()

    def get_sheet(self):
        response = requests.get(url=self.API_SHEET_URL_GET, headers=self.HEADER)
        response.raise_for_status()
        return response.json()

    def update_iata_in_record(self):
        for city in self.records["prices"]:
            city["iataCode"] = self.flight_search.get_iata(city_name=city["city"])

    def update_sheet(self):
        self.update_iata_in_record()
        for city in self.records["prices"]:
            json = {
                "price": {
                    "city": city["city"].title(),
                    "iataCode": city["iataCode"].title(),
                    "lowestPrice": city["lowestPrice"],
                    "id": city["id"]
                }
            }
            response = requests.put(url=self.API_SHEET_URL_PUT + f"{city["id"]}", headers=self.HEADER, json=json)
            response.raise_for_status()
            print(response.text)

    def get_record(self):
        return self.records["prices"]