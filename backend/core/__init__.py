# core/__init__.py
"""
Core module for simple multi-agent communication system
"""
from .simple_agent_router import SimpleAgentRouter
from .simple_websocket_handler import SimpleWebSocketHandler

__all__ = ["SimpleAgentRouter", "SimpleWebSocketHandler"]