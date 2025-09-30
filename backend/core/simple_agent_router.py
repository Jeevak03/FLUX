# core/simple_agent_router.py
"""
Simple Agent Router - Direct agent communication without LangGraph complexity
"""
import asyncio
import re
from typing import Dict, List, Optional, Tuple
from datetime import datetime

from agents.requirements_analyst import RequirementsAnalyst
from agents.software_architect import SoftwareArchitect
from agents.developer_agent import DeveloperAgent
from agents.qa_tester import QATester
from agents.devops_engineer import DevOpsEngineer
from agents.project_manager import ProjectManager
from agents.security_expert import SecurityExpert


class SimpleAgentRouter:
    """
    Extremely simple agent router that directly calls agents without complex workflows.
    No caching, no complex state, just direct routing based on message content.
    """
    
    def __init__(self):
        print("[ROUTER] 🚀 Initializing SimpleAgentRouter (NO LANGGRAPH)")
        
        # Initialize all agents once
        self.agents = {
            "sara": RequirementsAnalyst(),
            "marc": SoftwareArchitect(),
            "alex": DeveloperAgent(),
            "jess": QATester(),
            "dave": DevOpsEngineer(),
            "emma": ProjectManager(),
            "robt": SecurityExpert(),
        }
        
        # Simple name mappings - no regex complexity
        self.agent_names = {
            # Primary names
            "sara": "sara",
            "marc": "marc", 
            "alex": "alex",
            "jess": "jess",
            "dave": "dave",
            "emma": "emma",
            "robt": "robt",
            "rob": "robt",  # Rob -> Robt
            
            # Full names
            "sara requirements": "sara",
            "marc architect": "marc",
            "alex developer": "alex", 
            "jess tester": "jess",
            "dave devops": "dave",
            "emma manager": "emma",
            "robt security": "robt",
            "robert": "robt",
            
            # Variations
            "sarah": "sara",
            "marcus": "marc",
            "alexander": "alex",
            "jessica": "jess", 
            "david": "dave",
            "emily": "emma",
            "robert": "robt"
        }
        
        print(f"[ROUTER] ✅ Loaded {len(self.agents)} agents: {list(self.agents.keys())}")
    
    def detect_called_agent(self, message: str) -> Optional[str]:
        """
        Detect which agent is being called from a message.
        Returns agent key (sara, marc, etc.) or None if no direct call detected.
        """
        message_lower = message.lower().strip()
        
        print(f"[ROUTER] 🔍 Detecting agent in: '{message}'")
        
        # Check for direct greetings first (highest priority)
        greeting_patterns = [
            r'\bhi\s+(\w+)',
            r'\bhello\s+(\w+)', 
            r'\bhey\s+(\w+)',
            r'\bgreetings\s+(\w+)'
        ]
        
        for pattern in greeting_patterns:
            match = re.search(pattern, message_lower)
            if match:
                name = match.group(1)
                if name in self.agent_names:
                    agent_key = self.agent_names[name]
                    print(f"[ROUTER] ✅ DIRECT GREETING: '{name}' → {agent_key}")
                    return agent_key
                    
        # Check for name mentions in message
        for name_variant, agent_key in self.agent_names.items():
            if name_variant in message_lower:
                # Make sure it's a word boundary to avoid false matches
                if re.search(r'\b' + re.escape(name_variant) + r'\b', message_lower):
                    print(f"[ROUTER] ✅ NAME MENTION: '{name_variant}' → {agent_key}")
                    return agent_key
        
        print(f"[ROUTER] ❌ NO AGENT DETECTED in: '{message}'")
        return None
    
    def detect_team_call(self, message: str) -> bool:
        """Check if message is calling the whole team"""
        message_lower = message.lower().strip()
        team_keywords = ['everyone', 'everybody', 'team', 'all agents', 'all of you', 'entire team']
        
        for keyword in team_keywords:
            if keyword in message_lower:
                print(f"[ROUTER] 👥 TEAM CALL DETECTED: '{keyword}'")
                return True
        return False
    
    async def route_message(self, message: str, context: dict = None, requested_agents: List[str] = None) -> Dict[str, str]:
        """
        Route a message to appropriate agents and return their responses.
        This is the main entry point that replaces the entire LangGraph workflow.
        """
        print(f"\n{'='*60}")
        print(f"[ROUTER] 📨 ROUTING MESSAGE: '{message}'")
        print(f"[ROUTER] 👥 Requested agents: {requested_agents}")
        print(f"{'='*60}")
        
        responses = {}
        context = context or {}
        
        # Step 1: Check for direct agent call
        called_agent = self.detect_called_agent(message)
        if called_agent:
            print(f"[ROUTER] 🎯 DIRECT CALL to {called_agent}")
            agent = self.agents[called_agent]
            
            try:
                response = await agent.process_request(message, context)
                responses[called_agent] = response
                print(f"[ROUTER] ✅ {called_agent} responded: {len(response)} chars")
            except Exception as e:
                error_msg = f"Error from {called_agent}: {str(e)}"
                responses[called_agent] = error_msg
                print(f"[ROUTER] ❌ {called_agent} error: {e}")
            
            return responses
        
        # Step 2: Check for team call
        if self.detect_team_call(message) or (requested_agents and len(requested_agents) > 1):
            print(f"[ROUTER] 👥 TEAM COLLABORATION MODE")
            target_agents = requested_agents if requested_agents else list(self.agents.keys())
            
            # Process all agents in parallel
            tasks = []
            for agent_key in target_agents:
                if agent_key in self.agents:
                    agent = self.agents[agent_key]
                    task = agent.process_request(message, context)
                    tasks.append((agent_key, task))
            
            if tasks:
                print(f"[ROUTER] 🚀 Running {len(tasks)} agents in parallel")
                results = await asyncio.gather(*[task for _, task in tasks], return_exceptions=True)
                
                for (agent_key, _), result in zip(tasks, results):
                    if isinstance(result, Exception):
                        responses[agent_key] = f"Error: {str(result)}"
                        print(f"[ROUTER] ❌ {agent_key} error: {result}")
                    else:
                        responses[agent_key] = result
                        print(f"[ROUTER] ✅ {agent_key} responded: {len(result)} chars")
            
            return responses
        
        # Step 3: Smart single agent selection based on message content
        selected_agent = self._select_best_agent(message)
        if selected_agent:
            print(f"[ROUTER] 🤖 SMART SELECTION: {selected_agent}")
            agent = self.agents[selected_agent]
            
            try:
                response = await agent.process_request(message, context)
                responses[selected_agent] = response
                print(f"[ROUTER] ✅ {selected_agent} responded: {len(response)} chars")
            except Exception as e:
                error_msg = f"Error from {selected_agent}: {str(e)}"
                responses[selected_agent] = error_msg
                print(f"[ROUTER] ❌ {selected_agent} error: {e}")
        else:
            # Default to Sara only if absolutely no other option
            print(f"[ROUTER] 🎯 DEFAULT to Sara (Requirements Analyst)")
            try:
                response = await self.agents["sara"].process_request(message, context)
                responses["sara"] = response
                print(f"[ROUTER] ✅ Sara responded: {len(response)} chars")
            except Exception as e:
                responses["sara"] = f"Error: {str(e)}"
                print(f"[ROUTER] ❌ Sara error: {e}")
        
        return responses
    
    def _select_best_agent(self, message: str) -> Optional[str]:
        """
        Select the best agent based on message content keywords.
        This replaces complex LangGraph routing logic.
        """
        message_lower = message.lower()
        
        # Keywords for each agent
        agent_keywords = {
            "sara": ["requirement", "requirements", "specification", "spec", "user story", "acceptance criteria", "business rule"],
            "marc": ["architecture", "design", "system", "structure", "component", "module", "pattern", "framework"],
            "alex": ["code", "coding", "implement", "development", "programming", "function", "class", "method", "algorithm"],
            "jess": ["test", "testing", "quality", "bug", "issue", "validation", "verification", "qa", "quality assurance"],
            "dave": ["deploy", "deployment", "infrastructure", "server", "cloud", "docker", "kubernetes", "devops", "ci/cd"],
            "emma": ["project", "management", "timeline", "schedule", "milestone", "resource", "planning", "coordination"],
            "robt": ["security", "vulnerability", "authentication", "authorization", "encryption", "protection", "secure"]
        }
        
        # Score each agent based on keyword matches
        scores = {}
        for agent_key, keywords in agent_keywords.items():
            score = sum(1 for keyword in keywords if keyword in message_lower)
            if score > 0:
                scores[agent_key] = score
        
        if scores:
            best_agent = max(scores, key=scores.get)
            print(f"[ROUTER] 📊 Keyword scoring: {scores} → {best_agent}")
            return best_agent
        
        return None