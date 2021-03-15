from app.db import Base
from sqlalchemy import Column, String


class Consumer(Base):
    phone = Column(String(64), primary_key=True, nullable=False)
    phonetype = Column(String(64), nullable=False)
    voiceassistance = Column(String(64), nullable=False)
