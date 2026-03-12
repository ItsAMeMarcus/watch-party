from fastapi import WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
from repositories.room_repository import RoomRepository
from services.connection_manager import manager

class RoomService:
    def __init__(self, db: Session):
        self.repo = RoomRepository(db)

    def create_room(self, video_url: str):
        """
        Contém a lógica de negócio para criar uma sala.
        """
        if "youtube.com" not in video_url and "youtu.be" not in video_url:
            raise ValueError("O link fornecido não parece ser um vídeo válido do YouTube.")
        
        return self.repo.create(video_url)

    def get_room(self, room_id: str):
        """
        Busca a sala e aplica a regra de negócio caso ela não exista.
        """
        room = self.repo.get_by_id(room_id)
        
        if not room:
            raise ValueError("Sala não encontrada ou expirada.")
            
        return room

    async def join_live_room(self, websocket: WebSocket, room_id: str):
        """
        Método padronizado para gerenciar a entrada e sincronização na sala de vídeo.
        """
        room = self.repo.get_by_id(room_id)
        
        if not room:
            await websocket.close(code=1008, reason="Sala não encontrada")
            return

        await manager.connect(websocket, room_id)
        
        try:
            while True:
                data = await websocket.receive_json()
                await manager.broadcast(data, room_id)
                
        except WebSocketDisconnect:
            await manager.disconnect(websocket, room_id)
