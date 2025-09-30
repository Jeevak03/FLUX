# core/simple_websocket_handler.py
"""
Simple WebSocket Handler - Direct message routing without complex workflow management
"""
import json
import asyncio
from datetime import datetime
from typing import Dict, Any, List

from utils.websocket_manager import WebSocketManager
from utils.session_manager import SessionManager
from core.simple_agent_router import SimpleAgentRouter
from models.schemas import UserRequest, AgentMessage


class SimpleWebSocketHandler:
    """
    Simplified WebSocket handler that routes messages directly to agents
    without complex workflow state management or LangGraph overhead.
    """
    
    def __init__(self, websocket_manager: WebSocketManager, session_manager: SessionManager):
        self.websocket_manager = websocket_manager
        self.session_manager = session_manager
        self.router = SimpleAgentRouter()
        print("[WS-HANDLER] 🚀 SimpleWebSocketHandler initialized")
    
    async def handle_message(self, session_id: str, message_data: dict) -> None:
        """
        Handle incoming WebSocket message with simple, direct routing.
        No complex state management or workflow orchestration.
        """
        try:
            print(f"\n{'='*60}")
            print(f"[WS-HANDLER] 📨 Message received for session: {session_id}")
            print(f"[WS-HANDLER] 📝 Raw data: {message_data}")
            print(f"{'='*60}")
            
            # Parse user request
            try:
                user_request = UserRequest(**message_data)
            except Exception as e:
                await self._send_error(session_id, f"Invalid request format: {e}")
                return
            
            # Update session with latest request
            self.session_manager.update_session(session_id, {
                "last_request": user_request.dict(),
                "project_context": user_request.context.dict() if user_request.context else {}
            })
            
            # Send processing status
            await self.websocket_manager.send_status_update(
                session_id, "processing", "Processing your request..."
            )
            
            # Extract context information
            context = {
                "project_context": user_request.context.dict() if user_request.context else {},
                "conversation_history": [msg.dict() for msg in user_request.history],
                "uploaded_files": [file.dict() for file in user_request.uploaded_files],
                "timestamp": datetime.now().isoformat()
            }
            
            print(f"[WS-HANDLER] 🎯 Routing message: '{user_request.request}'")
            print(f"[WS-HANDLER] 👥 Requested agents: {user_request.requested_agents}")
            
            # Route message using simple router (NO LANGGRAPH)
            try:
                responses = await self.router.route_message(
                    message=user_request.request,
                    context=context,
                    requested_agents=user_request.requested_agents
                )
                
                print(f"[WS-HANDLER] ✅ Got {len(responses)} responses: {list(responses.keys())}")
                
                # Send each response immediately
                for agent_key, response in responses.items():
                    await self._send_agent_response(session_id, agent_key, response, user_request)
                
                # Send completion status
                agent_names = list(responses.keys())
                completion_msg = f"Completed with responses from: {', '.join(agent_names)}"
                await self.websocket_manager.send_status_update(
                    session_id, "completed", completion_msg
                )
                
                # Update session completion
                self.session_manager.update_session(session_id, {
                    "last_completion": datetime.now().isoformat(),
                    "last_agents": agent_names
                })
                
            except Exception as routing_error:
                print(f"[WS-HANDLER] ❌ Routing error: {routing_error}")
                await self._send_error(session_id, f"Error processing request: {routing_error}")
        
        except Exception as e:
            print(f"[WS-HANDLER] ❌ Fatal error handling message: {e}")
            await self._send_error(session_id, f"Internal error: {e}")
    
    async def _send_agent_response(self, session_id: str, agent_key: str, response: str, user_request: UserRequest) -> None:
        """Send agent response via WebSocket and update session history"""
        try:
            # Convert agent key to display name
            agent_display_names = {
                "sara": "Sara (Requirements Analyst)",
                "marc": "Marc (Software Architect)", 
                "alex": "Alex (Developer)",
                "jess": "Jess (QA Tester)",
                "dave": "Dave (DevOps Engineer)",
                "emma": "Emma (Project Manager)",
                "robt": "Robt (Security Expert)"
            }
            
            display_name = agent_display_names.get(agent_key, agent_key)
            
            print(f"[WS-HANDLER] 📤 Sending response from {display_name}: {len(response)} chars")
            
            # Send via WebSocket
            await self.websocket_manager.send_agent_response(session_id, display_name, response)
            
            # Add to session history
            message = AgentMessage(
                type="agent_response",
                agent=display_name,
                message=response,
                timestamp=datetime.now().isoformat()
            )
            self.session_manager.add_message_to_history(session_id, message.dict())
            
            # Broadcast collaboration if multiple agents active
            if len(user_request.requested_agents) > 1:
                await self.websocket_manager.broadcast_collaboration(
                    session_id, user_request.requested_agents, "active"
                )
                
        except Exception as e:
            print(f"[WS-HANDLER] ❌ Error sending agent response: {e}")
    
    async def _send_error(self, session_id: str, error_message: str) -> None:
        """Send error message via WebSocket"""
        try:
            await self.websocket_manager.send_agent_response(session_id, "system", error_message, "error")
            await self.websocket_manager.send_status_update(session_id, "error", "Please try again")
        except Exception as e:
            print(f"[WS-HANDLER] ❌ Error sending error message: {e}")