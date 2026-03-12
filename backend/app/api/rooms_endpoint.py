from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
from schemas.room import RoomCreate, RoomResponse
from infrastructure.database import get_db
from services.room_service import RoomService
from services.connection_manager import manager

router = APIRouter()

@router.post("/rooms", response_model=RoomResponse)
async def create_room(
    room_data: RoomCreate, 
    db: Session = Depends(get_db) 
):
    service = RoomService(db)
    try:
        new_room = service.create_room(room_data.video_url)
        return {"room_id": new_room.id, "video_url": new_room.video_url}
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))


@router.get("/rooms/{room_id}", response_model=RoomResponse)
async def get_room(
    room_id: str, 
    db: Session = Depends(get_db) 
):
    """
    Busca as informações de uma sala específica pelo seu ID.
    É usado quando um convidado abre o link de convite.
    """
    try:
        service = RoomService(db)
        room = service.get_room(room_id)
        return {"room_id": room.id, "video_url": room.video_url}

    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error))
        
@router.websocket("/ws/{room_id}")
async def websocket_endpoint(
    websocket: WebSocket, 
    room_id: str,
    db: Session = Depends(get_db) 
    ):
    """
    Endpoint de conexão em tempo real. O frontend se conecta aqui.
    """
    service = RoomService(db)
    
    # O Serviço assume o controle daqui para frente!
    await service.join_live_room(websocket, room_id)
