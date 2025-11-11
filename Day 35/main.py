#Unix time: seconds since Jan 1st, 1970

from forecast import Forecast
from bot import Bot

forecast = Forecast()
bot = Bot(forecast.get_forecast())