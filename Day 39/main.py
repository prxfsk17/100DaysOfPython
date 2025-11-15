#This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the program requirements.
import datetime

import requests
import os
from dotenv import load_dotenv

load_dotenv()

def get_token():
    url = "https://test.api.amadeus.com/v1/security/oauth2/token"

    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    data = {
        "grant_type": "client_credentials",
        "client_id": os.getenv("FLIGHT_API_KEY"),
        "client_secret": os.getenv("FLIGHT_API_SECRET")
    }
    response=requests.post(url=url,headers=headers,data=data)
    response.raise_for_status()
    return response.json()["access_token"]

def get_cheapest_among_flights(flights):
    if len(flights) != 171:
        try:
            flights = flights["data"]
        except KeyError:
            return None
    if len(flights)>0:
        returned_flight=flights[0]
        min_price = flights[0]["price"]["grandTotal"]
        for flight in flights:
            if flight["price"]["grandTotal"] < min_price:
                min_price=flight["price"]["grandTotal"]
                returned_flight=flight
        return returned_flight
    else:
        return None


def get_cheapest_flight_on_day(date, origin_code, destination):
    url=os.getenv("FLIGHT_API_URL")
    parameters={
        "originLocationCode" : origin_code,
        "destinationLocationCode" : destination,
        "departureDate" : date,
        "adults" : 1,
        "travelClass" : "ECONOMY",
        "nonStop" : "true",
        "currencyCode" : "EUR"
    }
    head = {
        "Authorization": f"Bearer {get_token()}"
    }
    response = requests.get(url=url, headers=head, params=parameters)
    response.raise_for_status()
    return get_cheapest_among_flights(response.json())

def get_cheapest_on_interval(origin_code, destination_code):
    print(f"Getting flights for {destination_code}...")
    today = datetime.datetime.now() + datetime.timedelta(days=1)
    flights=[get_cheapest_flight_on_day(today.strftime("%Y-%m-%d"), origin_code, destination_code)]
    for i in range(0, 170):
        tomorrow = today + datetime.timedelta(days=1)
        tomorrow_flight=get_cheapest_flight_on_day(tomorrow.strftime("%Y-%m-%d"), origin_code, destination_code)
        flights.append(tomorrow_flight)
        today=tomorrow
        print(tomorrow.strftime("%Y-%m-%d"), flights[i]["price"]["grandTotal"])
    the_cheapest = get_cheapest_among_flights(flights)
    print(f"{destination_code}: {the_cheapest["price"]["grandTotal"]} EUR.")


def get_iata(city_name):
    url = "https://test.api.amadeus.com/v1/reference-data/locations/cities"
    params = {
        "keyword" : f"{city_name}",
        "max" : 10,
        "include" : "AIRPORTS"
    }
    head = {
        "Authorization": f"Bearer {get_token()}"
    }
    response=requests.get(url=url,headers=head,params=params)
    response.raise_for_status()
    return response.json()["data"][0]["iataCode"]

def get_sheet():
    url=os.getenv("API_SHEET_URL")
    head={
        "Authorization" : os.getenv("API_SHEET_TOKEN")
    }
    response=requests.get(url=url, headers=head)
    response.raise_for_status()
    return response.json()

def update_sheet(new_records):
    url = os.getenv("API_SHEET_URL") + "/"
    head = {
        "Authorization": os.getenv("API_SHEET_TOKEN")
    }
    for City in new_records["prices"]:
        json = {
            "price" : {
                "city" : City["city"].title(),
                "iataCode" : City["iataCode"].title(),
                "lowestPrice" : City["lowestPrice"],
                "id" : City["id"]
            }
        }
        response=requests.put(url=url+f"{City["id"]}", headers=head, json=json)
        response.raise_for_status()
        print(response.text)

origin = os.getenv("AIR_CODE_DEPARTURE")
get_cheapest_on_interval(origin, "PAR")

# records = get_sheet()
# records = {'prices': [{'city': 'Paris', 'iataCode': 'PAR', 'lowestPrice': 100, 'id': 2}, {'city': 'Frankfurt', 'iataCode': 'FRA', 'lowestPrice': 230, 'id': 3}, {'city': 'Tokyo', 'iataCode': 'TYO', 'lowestPrice': 1000, 'id': 4}, {'city': 'Hong Kong', 'iataCode': 'HKG', 'lowestPrice': 860, 'id': 5}, {'city': 'Istanbul', 'iataCode': 'IST', 'lowestPrice': 227, 'id': 6}, {'city': 'Kuala Lumpur', 'iataCode': 'KUL', 'lowestPrice': 1003, 'id': 7}, {'city': 'New York', 'iataCode': 'NYC', 'lowestPrice': 825, 'id': 8}, {'city': 'San Francisco', 'iataCode': 'SFO', 'lowestPrice': 658, 'id': 9}, {'city': 'Dublin', 'iataCode': 'DBN', 'lowestPrice': 231, 'id': 10}, {'city': 'Vienna', 'iataCode': 'VIE', 'lowestPrice': 289, 'id': 11}, {'city': 'Prague', 'iataCode': 'PRG', 'lowestPrice': 557, 'id': 12}]}
# for city in records["prices"]:
#     city["iataCode"] = get_iata(city_name=city["city"])
# print(records)
# update_sheet(records)
# records = {'prices': [{'city': 'Paris', 'iataCode': 'PAR', 'lowestPrice': 100, 'id': 2}, {'city': 'Frankfurt', 'iataCode': 'FRA', 'lowestPrice': 230, 'id': 3}, {'city': 'Tokyo', 'iataCode': 'TYO', 'lowestPrice': 1000, 'id': 4}, {'city': 'Hong Kong', 'iataCode': 'HKG', 'lowestPrice': 860, 'id': 5}, {'city': 'Istanbul', 'iataCode': 'IST', 'lowestPrice': 227, 'id': 6}, {'city': 'Kuala Lumpur', 'iataCode': 'KUL', 'lowestPrice': 1003, 'id': 7}, {'city': 'New York', 'iataCode': 'NYC', 'lowestPrice': 825, 'id': 8}, {'city': 'San Francisco', 'iataCode': 'SFO', 'lowestPrice': 658, 'id': 9}, {'city': 'Dublin', 'iataCode': 'DBN', 'lowestPrice': 231, 'id': 10}, {'city': 'Vienna', 'iataCode': 'VIE', 'lowestPrice': 289, 'id': 11}, {'city': 'Prague', 'iataCode': 'PRG', 'lowestPrice': 557, 'id': 12}]}
# update_sheet(records)





# def get_flights():
#     url="https://test.api.amadeus.com/v1/shopping/flight-destinations"
#     head={
#         "Authorization" : f"Bearer {get_token()}"
#     }
#     json={
#         "origin" : "BER",
#         "oneWay" : True,
#         "maxPrice" : 200
#     }
#     response=requests.get(url=url, headers=head, params=json)
#     response.raise_for_status()
#     print(response.json())


