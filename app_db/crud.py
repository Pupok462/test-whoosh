from sqlalchemy.orm import Session as SessionType
from .models import History
from datetime import datetime, timedelta
from modules.openweather_request import fetch_weather
import numpy as np


def create_weather(session: SessionType, temperature: float):
    """
    Creates an entry in the database
    :param session:
    :param temperature: temperature from openweather
    :return: nothing
    """
    weather = History(temp=temperature, date=datetime.now())
    session.add(weather)
    session.commit()


def get_weather_history(session: SessionType):
    """

    :param session:
    :return: average temperature from some days
    """
    raw_history: list[History] = (
        session.query(History)
    ).all()
    if len(raw_history) == 0:
        return "Database is empty"
    result = []
    buff = []
    this_day = ''
    for h in raw_history:
        if len(buff) == 0:
            buff.append(h.temp)
            this_day = h.date.date()
            continue
        if h.date.date() == this_day:
            buff.append(h.temp)
        else:
            day_temp = np.average(buff)
            result.append({this_day: {"temp": day_temp}})
            if (h.date.date() - this_day).days > 1:
                for i in range(1, (h.date.date() - this_day).days):
                    result.append({this_day + timedelta(days=i): {"temp": 0.0}})
            print(buff)
            buff = []
            this_day = h.date.date()
            buff.append(h.temp)
    if len(buff) != 0:
        day_temp = np.average(buff)
        result.append({this_day: {"temp": day_temp}})
    return result

def get_temperature(session: SessionType):
    """
    Get temperature from OpenWeather and update db if current time - update time in db > 3600
    Else take the last temp from db
    :param session:
    :return: int(temperature)
    """
    history: list[History] = session.query(History).all()
    if len(history) == 0:
        temperature = fetch_weather()
        create_weather(session, temperature)
        return temperature
    if (int(datetime.now().timestamp()) - int(history[-1].date.timestamp())) > 3600:
        temperature = fetch_weather()
        create_weather(session, temperature)
        session.commit()
        return temperature
    else:
        return history[-1].temp

