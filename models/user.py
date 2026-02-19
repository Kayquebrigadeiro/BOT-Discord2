from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Usuario(Base):
    __tablename__ = 'usuarios'
    id = Column(Integer, primary_key=True)
    discord_id = Column(String, unique=True, nullable=False)
    nome = Column(String, nullable=False)
    active_queue = Column(Boolean, default=False)
    banned = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)