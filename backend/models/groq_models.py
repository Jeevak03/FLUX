# models/groq_models.py
from groq import Groq
from typing import Dict, Any, List, Optional
import os
import time
import json
from functools import lru_cache

class GroqModelManager:
    def __init__(self):
        # Ensure environment variables are loaded
        from dotenv import load_dotenv
        load_dotenv()
        
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY environment variable is required")
        self.client = Groq(api_key=api_key)
        
        # Response cache for common queries (simple in-memory cache)
        self._cache = {}
        self._cache_ttl = 300  # 5 minutes

        # Different models for different SDLC roles - Using 5 unique text generation models (Whisper excluded as it's audio-only)
        self.model_mapping = {
            "requirements_analyst": "llama-3.3-70b-versatile",           # Advanced analysis capabilities for complex requirement gathering
            "software_architect": "llama-3.1-8b-instant",               # Fast architectural decisions and system design  
            "developer": "openai/gpt-oss-120b",                         # Code generation and development tasks with high context (131K tokens)
            "qa_tester": "openai/gpt-oss-20b",                          # Thorough testing analysis and quality assurance (65K max completion)
            "devops_engineer": "meta-llama/llama-guard-4-12b",          # Infrastructure and deployment with safety focus (20MB file support)
            "project_manager": "llama-3.1-8b-instant",                  # Quick project decisions and coordination (reusing for speed)
            "security_expert": "llama-3.3-70b-versatile"               # Security analysis and recommendations (reusing for expertise)
        }

    def _get_cache_key(self, role: str, messages: List[Dict], temperature: float) -> str:
        """Generate cache key for request"""
        # Simple cache key based on role and last user message
        if messages and len(messages) > 1:
            user_msg = messages[-1].get('content', '')[:100]  # First 100 chars
            return f"{role}_{hash(user_msg)}_{temperature}"
        return None

    def _is_cache_valid(self, timestamp: float) -> bool:
        """Check if cached response is still valid"""
        return time.time() - timestamp < self._cache_ttl

    async def get_completion(self, role: str, messages: list, temperature: float = 0.7, use_cache: bool = False):
        model = self.model_mapping.get(role, "llama-3.1-8b-instant")
        
        try:
            print(f"[GROQ] Requesting completion for {role} using {model}")
            completion = self.client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=1024,  # Reduced from 4096 to avoid token limit errors
                stream=True  # Always use streaming for better perceived performance
            )
            
            return completion
        except Exception as e:
            print(f"[GROQ] Error for {role} with {model}: {e}")
            raise

    def warm_up_models(self):
        """Pre-warm models with simple requests for faster first responses"""
        print("[WARMUP] Starting model warm-up...")
        warm_up_messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Hello"}
        ]
        
        for role in ["requirements_analyst", "software_architect", "developer"]:
            try:
                # Fire and forget warm-up requests
                model = self.model_mapping.get(role, "llama-3.1-8b-instant")
                self.client.chat.completions.create(
                    model=model,
                    messages=warm_up_messages,
                    temperature=0.1,
                    max_tokens=10,
                    stream=False
                )
                print(f"[WARMUP] Warmed up {role}")
            except Exception as e:
                print(f"[WARMUP] Failed to warm up {role}: {e}")