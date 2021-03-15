from app.db import Base
from sqlalchemy import Column, String, Integer


class Mission(Base):
    missionid = Column(Integer, primary_key=True, autoincrement=True)
    area = Column(String(32), nullable=False)
    date = Column(String(32), nullable=False)
    time = Column(String(32), nullable=False)
    recommend_phone = Column(String(32), nullable=False)
    recommend_voiceass = Column(String(32), nullable=False)
