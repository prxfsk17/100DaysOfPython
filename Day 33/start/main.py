import math
import time

from config import send_notification
import requests
from datetime import datetime

MY_LAT = 53.902472 # Your latitude
MY_LONG = 27.561823 # Your longitude

#Your position is within +5 or -5 degrees of the ISS position.
def is_iis_over_head(iss_lat, iss_lng):
    if math.fabs(MY_LAT-iss_lat) > 5 or math.fabs(MY_LONG-iss_lng):
        return False
    return True

def is_dark_over_head():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }
    response_t = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response_t.raise_for_status()
    data_t = response.json()
    sunrise = int(data_t["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data_t["results"]["sunset"].split("T")[1].split(":")[0])

    time_now = datetime.now().hour

    if sunrise <= time_now <= sunset:
        return False
    return True

response = requests.get(url="http://api.open-notify.org/iss-now.json")
response.raise_for_status()
data = response.json()

iss_latitude = float(data["iss_position"]["latitude"])
iss_longitude = float(data["iss_position"]["longitude"])


while True:
    time.sleep(60)
    if is_iis_over_head(iss_latitude, iss_longitude):
        if is_dark_over_head():
            send_notification()


