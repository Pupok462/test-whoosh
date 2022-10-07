from fastapi import APIRouter, Depends
from app_db.crud import get_temperature, get_weather_history
from app_db.database import SessionLocal, engine
from app_db import models


models.Base.metadata.create_all(bind=engine)

router = APIRouter()


def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


@router.get("/weather")
def get_weather(session: SessionLocal = Depends(get_session)):
    temp = get_temperature(session)
    return {"temp": temp}


@router.get("/history")
def get_history(session: SessionLocal = Depends(get_session)):
    result = get_weather_history(session)
    return result
