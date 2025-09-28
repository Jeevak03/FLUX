# utils/websocket_manager.py
from fastapi import WebSocket
from typing import Dict, List
import json
import asyncio
from datetime import datetime

class WebSocketManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
        self.session_agents: Dict[str, List[str]] = {}

    async def connect(self, websocket: WebSocket, session_id: str):
        await websocket.accept()
        self.active_connections[session_id] = websocket
        self.session_agents[session_id] = []

    def disconnect(self, session_id: str):
        if session_id in self.active_connections:
            del self.active_connections[session_id]
        if session_id in self.session_agents:
            del self.session_agents[session_id]

    async def send_agent_response(self, session_id: str, agent_name: str, message: str, message_type: str = "agent_response"):
        if session_id in self.active_connections:
            try:
                data = {
                    "type": message_type,
                    "agent": agent_name,
                    "message": message,
                    "timestamp": datetime.now().isoformat()
                }
                await self.active_connections[session_id].send_text(json.dumps(data))
            except Exception as e:
                print(f"[WS_MGR] Error sending agent response to {session_id}: {e}")
                # Remove broken connection
                self.disconnect(session_id)

    async def broadcast_collaboration(self, session_id: str, agents: List[str], status: str):
        if session_id in self.active_connections:
            data = {
                "type": "collaboration_update",
                "agents": agents,
                "status": status,
                "timestamp": datetime.now().isoformat()
            }
            await self.active_connections[session_id].send_text(json.dumps(data))

    async def send_status_update(self, session_id: str, status: str, details: str = ""):
        if session_id in self.active_connections:
            try:
                data = {
                    "type": "status_update",
                    "status": status,
                    "details": details,
                    "timestamp": datetime.now().isoformat()
                }
                await self.active_connections[session_id].send_text(json.dumps(data))
            except Exception as e:
                print(f"[WS_MGR] Error sending status update to {session_id}: {e}")
                self.disconnect(session_id)