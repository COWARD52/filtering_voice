from app.db import Base
from sqlalchemy import Column, String, ForeignKey, SmallInteger, Float, Integer
from sqlalchemy.orm import relationship


class Consumerattack(Base):
    eventid = Column(Integer, primary_key=True)
    consumer = relationship('Consumer')

    phone = Column(String(11), ForeignKey('consumer.phone'), nullable=False)

    attack_class = Column(SmallInteger, nullable=False)
    longitude = Column(Float(30), nullable=False)
    latitude = Column(Float(30), nullable=False)
