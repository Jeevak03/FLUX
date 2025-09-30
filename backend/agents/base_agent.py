# agents/base_agent.py
from abc import ABC, abstractmethod
from typing import List, Dict, Any
from models.groq_models import GroqModelManager

class BaseSDLCAgent(ABC):
    def __init__(self, name: str, role: str, expertise: List[str]):
        self.name = name
        self.role = role
        self.expertise = expertise
        self._groq_manager = None
        self.conversation_history = []

    @property
    def groq_manager(self):
        if self._groq_manager is None:
            self._groq_manager = GroqModelManager()
        return self._groq_manager

    @abstractmethod
    def get_system_prompt(self) -> str:
        pass

    async def process_request(self, user_input: str, context: Dict[str, Any]) -> str:
        # Check if this is a direct call to this agent
        is_direct_call = context.get("direct_call", False)
        interaction_type = context.get("interaction_type", "")
        
        # Prepare the context with uploaded files if available
        context_str = f"Context: {context}"
        
        # Add uploaded files to the context if they exist
        if 'uploaded_files' in context and context['uploaded_files']:
            context_str += "\n\nUPLOADED DOCUMENTS:\n"
            for i, file_info in enumerate(context['uploaded_files'], 1):
                context_str += f"\n{i}. FILE: {file_info.get('name', 'Unknown')}\n"
                context_str += f"   TYPE: {file_info.get('type', 'Unknown')}\n"
                context_str += f"   SIZE: {file_info.get('size', 0)} bytes\n"
                
                # Include file content with smart truncation
                content = file_info.get('content', '')
                if content and file_info.get('type', '').startswith(('text/', 'application/json')):
                    # For text files, truncate if too long (approximate token limit)
                    max_chars = 8000  # Roughly 2000 tokens worth of content
                    if len(content) > max_chars:
                        context_str += f"   CONTENT (truncated - showing first {max_chars} characters):\n{content[:max_chars]}...\n"
                        context_str += f"   [Note: File is {len(content)} characters total, truncated for processing]\n"
                    else:
                        context_str += f"   CONTENT:\n{content}\n"
                elif content and file_info.get('type') == 'application/pdf':
                    # For PDFs, provide a summary instead of full content
                    if len(content) > 8000:
                        context_str += f"   CONTENT SUMMARY: This is a PDF document. Key sections visible:\n{content[:2000]}...\n"
                        context_str += f"   [Note: PDF content truncated for processing - full document is {len(content)} characters]\n"
                    else:
                        context_str += f"   CONTENT: {content}\n"
                else:
                    context_str += f"   CONTENT: [Binary file - {file_info.get('type', 'unknown type')}]\n"
                context_str += "---\n"

        # Build system prompt with direct call context if applicable
        system_prompt = self.get_system_prompt()
        if is_direct_call:
            system_prompt += f"\n\nIMPORTANT: {interaction_type} Be conversational and personable, as if speaking directly to a colleague."

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"{context_str}\n\nRequest: {user_input}"}
        ]

        # Additional safety check - if context is still too large, truncate further
        total_length = len(self.get_system_prompt()) + len(context_str) + len(user_input)
        if total_length > 15000:  # Conservative limit to avoid token issues
            print(f"[AGENT] Warning: Context very large ({total_length} chars), truncating...")
            # Reduce context_str if needed
            if len(context_str) > 10000:
                context_str = context_str[:10000] + "\n[Context truncated for processing...]"
                messages[1]["content"] = f"{context_str}\n\nRequest: {user_input}"

        try:
            completion = await self.groq_manager.get_completion(
                role=self.role,
                messages=messages,
                temperature=0.7
            )

            # Handle streaming response from Groq
            full_response = ""
            try:
                for chunk in completion:
                    if hasattr(chunk, 'choices') and len(chunk.choices) > 0:
                        delta = chunk.choices[0].delta
                        if hasattr(delta, 'content') and delta.content:
                            full_response += delta.content
            except Exception as stream_err:
                print(f"[AGENT] Streaming error for {self.name}: {stream_err}")
                # Fallback: try to get the response as a whole
                if hasattr(completion, 'choices') and len(completion.choices) > 0:
                    message = completion.choices[0].message
                    if hasattr(message, 'content'):
                        full_response = message.content
            
            result = full_response.strip() if full_response else f"I'm {self.name}, ready to help with {self.role} tasks."
            print(f"[AGENT] {self.name} generated {len(result)} chars: {result[:100]}...")
            return result
            
        except Exception as e:
            error_msg = f"Error in {self.name}: {str(e)}"
            print(f"[AGENT] {error_msg}")
            return error_msg