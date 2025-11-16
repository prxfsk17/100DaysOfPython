import os
from dotenv import load_dotenv
import requests

class FlightSearch:
    #This class is responsible for talking to the Flight Search API.

    def __init__(self):
        load_dotenv()
        self.URL_IATA = os.getenv("URL_IATA")
        self.URL_TOKEN = os.getenv("URL_TOKEN")
        self.URL = os.getenv("FLIGHT_API_URL")

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

    def get_cheapest_flight_on_day(self, dprt_code, arrv_code, date, non_stop):
        parameters = {
            "originLocationCode": dprt_code,
            "destinationLocationCode": arrv_code,
            "departureDate": date,
            "adults": 1,
            "travelClass": "ECONOMY",
            "nonStop": non_stop,
            "currencyCode": "EUR"
        }
        head = {
            "Authorization": f"Bearer {self.get_token()}"
        }
        try:
            response = requests.get(url=self.URL, headers=head, params=parameters)
            response.raise_for_status()
            flights = response.json()["data"]
        except requests.exceptions.HTTPError:
            return None
        except TypeError:
            return None
        return self.get_cheapest_among_flights(flights)

    def get_cheapest_among_flights(self, flights):
        if len(flights) > 0:
            try:
                returned_flight = flights[0]
                min_price = flights[0]["price"]["grandTotal"]
            except TypeError:
                returned_flight=None
                min_price=1001
            for flight in flights:
                if not flight is None and flight["price"]["grandTotal"] < min_price:
                    try:
                        min_price = flight["price"]["grandTotal"]
                        returned_flight = flight
                    except TypeError:
                        continue
            return returned_flight
        else:
            return None

