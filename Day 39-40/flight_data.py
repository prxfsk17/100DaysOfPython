import datetime
import os
from dotenv import load_dotenv
from flight_search import FlightSearch

class FlightData:
    #This class is responsible for structuring the flight data.

    def __init__(self, arrival_code, arrival, lowest_price, fs : FlightSearch):
        load_dotenv()
        self.price = 0
        self.departure_airport_code=os.getenv("AIR_CODE_DEPARTURE")
        self.arrival_airport_code=arrival_code
        self.departure_name="Warsaw"
        self.arrival_name=arrival
        self.flight = None
        self.flight_search = fs
        self.lowest_price = lowest_price

    def get_cheapest_on_interval(self, non_stop="true"):
        print(f"Getting flights for {self.arrival_name}...")
        today = datetime.datetime.now() + datetime.timedelta(days=1)
        flights = [self.flight_search.get_cheapest_flight_on_day(self.departure_airport_code, self.arrival_airport_code, today.strftime("%Y-%m-%d"), non_stop)]
        for i in range(0, 30):
            tomorrow = today + datetime.timedelta(days=1)
            tomorrow_flight = self.flight_search.get_cheapest_flight_on_day(self.departure_airport_code, self.arrival_airport_code, tomorrow.strftime("%Y-%m-%d"), non_stop)
            #This feature created to decrease running time
            try:
                if float(tomorrow_flight["price"]["grandTotal"]) < self.lowest_price:
                    self.flight = tomorrow_flight
                    return self.flight
                flights.append(tomorrow_flight)
                today = tomorrow
                print(tomorrow.strftime("%Y-%m-%d"), tomorrow_flight["price"]["grandTotal"])
            except TypeError:
                print(tomorrow.strftime("%Y-%m-%d"))
                today = tomorrow
                continue
        self.flight = self.flight_search.get_cheapest_among_flights(flights)
        try:
            print(self.flight)
            print(f"{self.arrival_name}: {self.flight["price"]["grandTotal"]} EUR.")
            return self.flight
        except TypeError:
            if non_stop == "true":
                print(f"Getting flights with stopover for {self.arrival_name}...")
                return self.get_cheapest_on_interval("false")
            else:
                print(f"No flight data\n{self.arrival_name}: N/A")
                return None