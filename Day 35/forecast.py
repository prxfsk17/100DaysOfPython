import requests
import os

API_KEY_PY = os.environ.get("API_ENDPOINT")
INTERVAL_URL = os.environ.get("WEATHER_URL")
MINSK_LAT = 53.902472
MINSK_LNG = 27.561823
ROME_LAT = 41.902782
ROME_LNG = 12.496366

class Forecast:

    def __init__(self):

        self.parameters = {
            "lat" : ROME_LAT,
            "lon" : ROME_LNG,
            "cnt" : 4,
            "appid" : API_KEY_PY
        }
        self.codes_list = []

    def get_forecast(self):
        response = requests.get(INTERVAL_URL, params=self.parameters)
        response.raise_for_status()

        data = response.json()
        weather_list = data["list"]
        self.codes_list = [item["weather"][0]["id"] for item in weather_list]
        return self.is_rain_in_twelve_hours()

    def is_rain_in_twelve_hours(self) -> bool:
        for condition in self.codes_list:
            if int(condition / 100) < 7:
                return True
        return False