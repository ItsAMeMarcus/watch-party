from sqlalchemy.orm import Session
from models.room_model import Room
import uuid

class RoomRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, video_url: str) -> Room:
        """Cria uma nova sala no banco de dados e retorna a entidade."""
        # Gera o ID único
        room_id = str(uuid.uuid4())[:8]
        
        # Prepara o objeto para salvar
        db_room = Room(id=room_id, video_url=video_url)
        
        # Adiciona e confirma (commit) a transação no banco
        self.db.add(db_room)
        self.db.commit()
        self.db.refresh(db_room) # Atualiza o objeto com os dados recém-salvos
        
        return db_room

    def get_by_id(self, room_id: str) -> Room | None:
        """Busca uma sala pelo ID. Retorna None se não achar."""
        return self.db.query(Room).filter(Room.id == room_id).first()
