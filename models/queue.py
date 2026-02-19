from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Fila(Base):
    __tablename__ = 'filas'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('usuarios.id'), nullable=False)
    valor = Column(Float, nullable=False)
    formato = Column(String, nullable=False)  # 1v1, 2v2, etc.
    status = Column(String, default='active')  # active, cancelled
    created_at = Column(DateTime, default=datetime.utcnow)