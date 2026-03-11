# app/models/room.py
from sqlalchemy import Column, String, DateTime
from infrastructure.database import Base
from datetime import datetime

class Room(Base):
    __tablename__ = "rooms" # Nome da tabela no banco de dados

    # Definindo as colunas
    id = Column(String, primary_key=True, index=True)
    video_url = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
