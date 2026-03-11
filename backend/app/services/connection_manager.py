from fastapi import WebSocket
import time

class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[str, list[dict]] = {}
        self.room_states: dict[str, dict] = {}

    async def connect(self, websocket: WebSocket, room_id: str, username: str = "Anônimo"):
        """Aceita a conexão e adiciona o usuário à sala correta."""
        await websocket.accept()
        if room_id not in self.active_connections:
            self.active_connections[room_id] = []
            self.room_states[room_id] = {
                "action": "pause", 
                "time": 0.0, 
                "updated_at": time.time()
            }
        self.active_connections[room_id].append({
            "ws": websocket,
            "username": username
        })
        current_state = self.room_states[room_id]
        calculated_time = current_state["time"]

        if current_state["action"] == "play":
            time_passed = time.time() - current_state["updated_at"]
            calculated_time += time_passed

        await websocket.send_json({
            "action": current_state["action"],
            "time": calculated_time
        })

    def disconnect(self, websocket: WebSocket, room_id: str):
        """Remove o usuário da sala quando ele fechar a página."""
        if room_id in self.active_connections:
            self.active_connections[room_id] = [
                conn for conn in self.active_connections[room_id] if conn["ws"] != websocket
            ]
            if not self.active_connections[room_id]:
                del self.active_connections[room_id]
                if room_id in self.room_states:
                    del self.room_states[room_id]

    async def broadcast(self, message: dict, room_id: str):
        """Envia uma mensagem (JSON) para todos os usuários da mesma sala."""
        
        if "action" in message and "time" in message:
            self.room_states[room_id] = {
                "action": message["action"],
                "time": message["time"],
                "updated_at": time.time() # Guarda a hora exata que a ação aconteceu
            }

        # 7. Repassa a mensagem para todos
        if room_id in self.active_connections:
            for connection in self.active_connections[room_id]:
                await connection["ws"].send_json(message)

    def get_user_count(self, room_id: str) -> int:
        """Retorna quantos usuários estão na sala para mostrar no frontend."""
        return len(self.active_connections.get(room_id, []))
    

# Instância global que será importada pelas rotas
manager = ConnectionManager()
