from sqlalchemy import Column, SmallInteger, String, Integer, Float, ForeignKey
from . import Base
from sqlalchemy.orm import relationship


class Volume(Base):
    volume_id = Column(Integer, primary_key=True, autoincrement=True)
    volume_filename = Column(String(50), nullable=False)
    attack_class = Column(SmallInteger, nullable=False)
    longitude = Column(Float(30), nullable=False)
    latitude = Column(Float(30), nullable=False)
    posi = Column(String(45))
    consumer = relationship('Consumer')
    phone = Column(String(64), ForeignKey('consumer.phone'), nullable=False)
