from pydantic import BaseModel

class RoomCreate(BaseModel):
    video_url: str 

class RoomResponse(BaseModel):
    room_id: str
    video_url: str
