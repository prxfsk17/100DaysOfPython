#This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the program requirements.

from data_manager import DataManager
from flight_search import FlightSearch
from flight_data import FlightData
from notification_manager import NotificationManager

flight_search_manager = FlightSearch()
data_manager = DataManager(flight_search_manager)
flight_data_manager = [FlightData(item["iataCode"], item["city"], item["lowestPrice"], flight_search_manager) for item in data_manager.get_record()]
notification_manager = NotificationManager()

print(data_manager.emails)

for flight in flight_data_manager:
    data = flight.get_cheapest_on_interval()
    if not data is None:
        if float(data["price"]["grandTotal"]) < flight.lowest_price:
            message=(f"Low price alert! Only {data["price"]["grandTotal"]} {data["price"]["currency"]} to fly from {data["itineraries"][0]["segments"][0]["departure"]["iataCode"]} "
                    f"to {data["itineraries"][0]["segments"][0]["arrival"]["iataCode"]}, on {data["itineraries"][0]["segments"][0]["departure"]["at"]}.")
            # notification_manager.send_message(message)
            for email in data_manager.get_emails():
                notification_manager.send_to_email(email, message)
            print(message)

