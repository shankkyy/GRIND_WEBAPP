from fastapi import WebSocket
from typing import Dict, List, Set
import json

class ConnectionManager:
    """Manages WebSocket connections for real-time updates"""
    
    def __init__(self):
        self.active_connections: Dict[str, List[WebSocket]] = {}  # room_id -> [websockets]
        self.user_connections: Dict[str, Dict[str, WebSocket]] = {}  # room_id -> {user_id: websocket}
        self.global_connections: Set[WebSocket] = set()  # Global connections for leaderboard, etc.
    
    async def connect(self, websocket: WebSocket, room_id: str, user_id: str):
        """Accept and register a new connection"""
        await websocket.accept()
        
        # Initialize room if not exists
        if room_id not in self.active_connections:
            self.active_connections[room_id] = []
            self.user_connections[room_id] = {}
        
        # Add connection
        self.active_connections[room_id].append(websocket)
        self.user_connections[room_id][user_id] = websocket
        
        # Notify others that user joined
        await self.broadcast_room(
            room_id=room_id,
            message={
                "type": "user_joined",
                "user_id": user_id
            },
            exclude_user=None
        )
    
    async def disconnect(self, room_id: str, user_id: str):
        """Disconnect a user"""
        if room_id in self.active_connections and user_id in self.user_connections[room_id]:
            websocket = self.user_connections[room_id][user_id]
            self.active_connections[room_id].remove(websocket)
            del self.user_connections[room_id][user_id]
            
            # Notify others that user left
            await self.broadcast_room(
                room_id=room_id,
                message={
                    "type": "user_left",
                    "user_id": user_id
                }
            )
    
    async def connect_global(self, websocket: WebSocket):
        """Connect to global broadcast (for leaderboard, etc.)"""
        await websocket.accept()
        self.global_connections.add(websocket)
    
    async def disconnect_global(self, websocket: WebSocket):
        """Disconnect from global broadcast"""
        self.global_connections.discard(websocket)
    
    async def broadcast_room(self, room_id: str, message: dict, exclude_user: str = None):
        """Broadcast message to all users in a room"""
        if room_id not in self.active_connections:
            return
        
        # Convert message to JSON
        if not isinstance(message, str):
            message = json.dumps(message)
        
        # Send to all connections in room
        dead_connections = []
        for user_id, websocket in self.user_connections[room_id].items():
            if exclude_user and user_id == exclude_user:
                continue
            
            try:
                await websocket.send_text(message)
            except Exception as e:
                print(f"Error sending to {user_id}: {e}")
                dead_connections.append((room_id, user_id))
        
        # Clean up dead connections
        for room, user in dead_connections:
            if user in self.user_connections.get(room, {}):
                del self.user_connections[room][user]
    
    async def broadcast(self, message: dict):
        """Broadcast message to all connections globally"""
        if not isinstance(message, str):
            message = json.dumps(message)
        
        dead_connections = []
        for websocket in self.global_connections:
            try:
                await websocket.send_text(message)
            except Exception as e:
                print(f"Error sending global message: {e}")
                dead_connections.append(websocket)
        
        # Clean up dead connections
        for ws in dead_connections:
            self.global_connections.discard(ws)
    
    async def send_personal_message(self, room_id: str, user_id: str, message: dict):
        """Send message to specific user"""
        if room_id not in self.user_connections or user_id not in self.user_connections[room_id]:
            return
        
        if not isinstance(message, str):
            message = json.dumps(message)
        
        try:
            await self.user_connections[room_id][user_id].send_text(message)
        except Exception as e:
            print(f"Error sending personal message: {e}")
    
    async def get_room_users(self, room_id: str) -> List[str]:
        """Get list of user IDs in a room"""
        if room_id not in self.user_connections:
            return []
        return list(self.user_connections[room_id].keys())
    
    async def get_room_count(self, room_id: str) -> int:
        """Get number of users in a room"""
        if room_id not in self.active_connections:
            return 0
        return len(self.active_connections[room_id])

# Global instance
manager = ConnectionManager()
