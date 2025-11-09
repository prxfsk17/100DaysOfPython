import requests
import datetime as dt

API_ENDPOINT = "http://api.open-notify.org/iss-now.json"
response = requests.get(url=API_ENDPOINT)
#response codes
#1XX - Hold on
#2XX - Here you go
#3XX - No permission, go away
#4XX - You screwed up
#404 - don't exist
#5XX - server screwed up
# if response.status_code == 404:
#     raise Exception("That resource does not exist.")
# elif response.status_code == 401:
#     raise Exception("You are not authorised to access this data. ")
response.raise_for_status()

data = response.json()["iss_position"]
longitude = float(data["longitude"])
latitude = float(data["latitude"])
# print(longitude, latitude)

MINSK_LAT = 53.902472
MINSK_LNG = 27.561823

parameters = {
    "lat" : MINSK_LAT,
    "lng" : MINSK_LNG,
    "formatted" : 0
}

API_SUNSET = "https://api.sunrise-sunset.org/json?}"
response_sunset = requests.get(url=API_SUNSET, params=parameters)
response_sunset.raise_for_status()
data_sunset = response_sunset.json()
sunrise = data_sunset["results"]["sunrise"].split("T")[1].split(":")[0]
sunset = data_sunset["results"]["sunset"].split("T")[1].split(":")[0]

print(sunrise)
print(sunset)

current_time = dt.datetime.now()
print(current_time.hour)



