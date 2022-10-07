import requests

API_KEY = "3353ea6359950871cdaa05bcdd026264"


def fetch_weather():
    """
    Fetching info from OPENWEATHER API
    :return: Moscow temperature in Celsius from json
    """
    url = 'https://api.openweathermap.org/data/2.5/weather'
    normalization: float = 274.15
    data = {
        "q": "Moscow",
        "appid": API_KEY,
    }
    temp = requests.get(url, params=data).json()["main"]["temp"] - normalization

    return float("{0:.2f}".format(temp))
