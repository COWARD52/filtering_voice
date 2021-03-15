from app.db import Base
from sqlalchemy import Column, String, ForeignKey, SmallInteger, Float, Integer
from sqlalchemy.orm import relationship


class Consumermission(Base):
    cmid = Column(Integer, primary_key=True, nullable=False)

    mission = relationship('Mission')
    missionid = Column(Integer, ForeignKey('mission.missionid'), nullable=False)

    consumer = relationship('Consumer')
    phone = Column(String(64), ForeignKey('consumer.phone'), nullable=False)

    agree = Column(Integer, nullable=False)
    huishou = Column(Integer, nullable=False)
