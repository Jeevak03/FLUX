# utils/session_manager.py
import redis
import json
from typing import Dict, Any, Optional, List
import os
from datetime import datetime, timedelta

class SessionManager:
    def __init__(self):
        try:
            self.redis_client = redis.Redis(
                host=os.getenv("REDIS_HOST", "localhost"),
                port=int(os.getenv("REDIS_PORT", 6379)),
                db=int(os.getenv("REDIS_DB", 0)),
                decode_responses=True,
                socket_connect_timeout=1,
                socket_timeout=1
            )
            # Test the connection
            self.redis_client.ping()
            self.redis_available = True
            print("Redis connection established")
        except (redis.ConnectionError, redis.TimeoutError, Exception):
            print("Redis not available, using in-memory storage")
            self.redis_available = False
            self.memory_storage = {}

    def create_session(self, session_id: str, initial_data: Dict[str, Any] = None) -> bool:
        """Create a new session with optional initial data"""
        try:
            session_data = {
                "created_at": datetime.now().isoformat(),
                "last_activity": datetime.now().isoformat(),
                "conversation_history": [],
                "project_context": {},
                "agent_outputs": {},
                "current_phase": "initial"
            }

            if initial_data:
                session_data.update(initial_data)

            if self.redis_available:
                self.redis_client.setex(
                    f"session:{session_id}",
                    timedelta(hours=24),  # 24 hour expiry
                    json.dumps(session_data)
                )
            else:
                self.memory_storage[session_id] = session_data
            return True
        except Exception as e:
            print(f"Error creating session: {e}")
            return False

    def get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve session data"""
        try:
            if self.redis_available:
                data = self.redis_client.get(f"session:{session_id}")
                if data:
                    session_data = json.loads(data)
                    # Update last activity
                    session_data["last_activity"] = datetime.now().isoformat()
                    self.redis_client.setex(
                        f"session:{session_id}",
                        timedelta(hours=24),
                        json.dumps(session_data)
                    )
                    return session_data
            else:
                if session_id in self.memory_storage:
                    session_data = self.memory_storage[session_id].copy()
                    session_data["last_activity"] = datetime.now().isoformat()
                    self.memory_storage[session_id] = session_data
                    return session_data
            return None
        except Exception as e:
            print(f"Error retrieving session: {e}")
            return None

    def update_session(self, session_id: str, updates: Dict[str, Any]) -> bool:
        """Update session data"""
        try:
            session_data = self.get_session(session_id)
            if session_data:
                session_data.update(updates)
                session_data["last_activity"] = datetime.now().isoformat()

                if self.redis_available:
                    self.redis_client.setex(
                        f"session:{session_id}",
                        timedelta(hours=24),
                        json.dumps(session_data)
                    )
                else:
                    self.memory_storage[session_id] = session_data
                return True
            return False
        except Exception as e:
            print(f"Error updating session: {e}")
            return False

    def add_message_to_history(self, session_id: str, message: Dict[str, Any]) -> bool:
        """Add a message to the conversation history"""
        try:
            session_data = self.get_session(session_id)
            if session_data:
                if "conversation_history" not in session_data:
                    session_data["conversation_history"] = []

                session_data["conversation_history"].append(message)

                # Keep only last 50 messages to prevent memory issues
                if len(session_data["conversation_history"]) > 50:
                    session_data["conversation_history"] = session_data["conversation_history"][-50:]

                return self.update_session(session_id, session_data)
            return False
        except Exception as e:
            print(f"Error adding message to history: {e}")
            return False

    def delete_session(self, session_id: str) -> bool:
        """Delete a session"""
        try:
            if self.redis_available:
                return bool(self.redis_client.delete(f"session:{session_id}"))
            else:
                if session_id in self.memory_storage:
                    del self.memory_storage[session_id]
                    return True
                return False
        except Exception as e:
            print(f"Error deleting session: {e}")
            return False

    def get_active_sessions(self) -> List[str]:
        """Get list of active session IDs"""
        try:
            if self.redis_available:
                keys = self.redis_client.keys("session:*")
                return [key.replace("session:", "") for key in keys]
            else:
                return list(self.memory_storage.keys())
        except Exception as e:
            print(f"Error getting active sessions: {e}")
            return []