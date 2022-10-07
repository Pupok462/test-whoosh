from sqlalchemy import Column, Float, Integer, DateTime
from .database import Base


class History(Base):
    __tablename__ = "History"

    date = Column(DateTime, unique=True)
    temp = Column(Float, default=0.0, unique=False)

    def __str__(self):
        return f"temp: {self.temp}| date: {self.date}"
