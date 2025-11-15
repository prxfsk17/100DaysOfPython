import datetime
import os
from dotenv import load_dotenv
import requests
from flight_search import FlightSearch

def get_cheapest_among_flights(flights):
    if len(flights) > 0:
        returned_flight = flights[0]
        min_price = flights[0]["price"]["grandTotal"]
        for flight in flights:
            if not flight is None and flight["price"]["grandTotal"] < min_price:
                min_price = flight["price"]["grandTotal"]
                returned_flight = flight
        return returned_flight
    else:
        return None


class FlightData:
    #This class is responsible for structuring the flight data.

    def __init__(self, arrival_code, arrival, fs):
        load_dotenv()
        self.price = 0
        self.departure_airport_code=os.getenv("AIR_CODE_DEPARTURE")
        self.arrival_airport_code=arrival_code
        self.departure_name="Warsaw"
        self.arrival_name=arrival
        self.URL=os.getenv("FLIGHT_API_URL")
        self.flight = None
        self.flight_search = fs

    def get_cheapest_on_interval(self):
        print(f"Getting flights for {self.arrival_name}...")
        today = datetime.datetime.now() + datetime.timedelta(days=1)
        flights = [self.get_cheapest_flight_on_day(today.strftime("%Y-%m-%d"))]
        for i in range(0, 170):
            tomorrow = today + datetime.timedelta(days=1)
            tomorrow_flight = self.get_cheapest_flight_on_day(tomorrow.strftime("%Y-%m-%d"))
            flights.append(tomorrow_flight)
            today = tomorrow
            print(tomorrow.strftime("%Y-%m-%d"), flights[i]["price"]["grandTotal"])
        self.flight = get_cheapest_among_flights(flights)
        print(f"{self.arrival_name}: {self.flight["price"]["grandTotal"]} EUR.")

    def get_cheapest_flight_on_day(self, date):
        parameters = {
            "originLocationCode": self.departure_airport_code,
            "destinationLocationCode": self.arrival_airport_code,
            "departureDate": date,
            "adults": 1,
            "travelClass": "ECONOMY",
            "nonStop": "true",
            "currencyCode": "EUR"
        }
        head = {
            "Authorization": f"Bearer {self.flight_search.get_token()}"
        }
        response = requests.get(url=self.URL, headers=head, params=parameters)
        response.raise_for_status()
        try:
            flights = response.json()["data"]
        except KeyError:
            return None
        return get_cheapest_among_flights(flights)

