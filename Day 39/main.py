#This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the program requirements.

from data_manager import DataManager
from flight_search import FlightSearch
from flight_data import FlightData
from notification_manager import NotificationManager

flight_search_manager = FlightSearch()
data_manager = DataManager(flight_search_manager)
flight_data_manager = [FlightData(item["iataCode"], item["city"], flight_search_manager) for item in data_manager.get_record()]
print(flight_data_manager)

# records = {'prices': [{'city': 'Paris', 'iataCode': 'PAR', 'lowestPrice': 100, 'id': 2}, {'city': 'Frankfurt', 'iataCode': 'FRA', 'lowestPrice': 230, 'id': 3}, {'city': 'Tokyo', 'iataCode': 'TYO', 'lowestPrice': 1000, 'id': 4}, {'city': 'Hong Kong', 'iataCode': 'HKG', 'lowestPrice': 860, 'id': 5}, {'city': 'Istanbul', 'iataCode': 'IST', 'lowestPrice': 227, 'id': 6}, {'city': 'Kuala Lumpur', 'iataCode': 'KUL', 'lowestPrice': 1003, 'id': 7}, {'city': 'New York', 'iataCode': 'NYC', 'lowestPrice': 825, 'id': 8}, {'city': 'San Francisco', 'iataCode': 'SFO', 'lowestPrice': 658, 'id': 9}, {'city': 'Dublin', 'iataCode': 'DBN', 'lowestPrice': 231, 'id': 10}, {'city': 'Vienna', 'iataCode': 'VIE', 'lowestPrice': 289, 'id': 11}, {'city': 'Prague', 'iataCode': 'PRG', 'lowestPrice': 557, 'id': 12}]}
