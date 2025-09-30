# workflows/sdlc_workflow.py
from langgraph.graph import StateGraph, END
from typing import TypedDict, List, Optional
import asyncio
import re

from agents.requirements_analyst import RequirementsAnalyst
from agents.software_architect import SoftwareArchitect
from agents.developer_agent import DeveloperAgent
from agents.qa_tester import QATester
from agents.devops_engineer import DevOpsEngineer
from agents.project_manager import ProjectManager
from agents.security_expert import SecurityExpert

class SDLCState(TypedDict):
    user_request: str
    current_phase: str
    agent_outputs: dict
    conversation_history: list
    project_context: dict
    uploaded_files: list  # Add support for uploaded files
    next_agent: str
    final_response: str
    requested_agents: list  # Agents requested by user
    called_agent: Optional[str]  # Specific agent directly called by user

class SDLCWorkflow:
    def __init__(self):
        self.agents = {
            "requirements_analyst": RequirementsAnalyst(),
            "software_architect": SoftwareArchitect(),
            "developer": DeveloperAgent(),
            "qa_tester": QATester(),
            "devops_engineer": DevOpsEngineer(),
            "project_manager": ProjectManager(),
            "security_expert": SecurityExpert()
        }

        self.workflow = self._create_workflow()

    def _create_workflow(self) -> StateGraph:
        workflow = StateGraph(SDLCState)

        # 🚨 NUCLEAR FIX: FORCE NEW WORKFLOW WITH HARDCODED ROUTING
        print("[WORKFLOW] 🔥 CREATING NUCLEAR WORKFLOW WITH HARDCODED ROUTING")
        
        # Add nodes for each SDLC phase
        workflow.add_node("route_entry", self._route_entry_point)  # New entry routing node
        workflow.add_node("analyze_requirements", self._analyze_requirements)
        workflow.add_node("design_architecture", self._design_architecture)
        workflow.add_node("develop_solution", self._develop_solution)
        workflow.add_node("test_solution", self._test_solution)
        workflow.add_node("plan_deployment", self._plan_deployment)
        workflow.add_node("manage_project", self._manage_project)
        workflow.add_node("security_review", self._security_review)
        workflow.add_node("collaborate", self._multi_agent_collaboration)

        # Define workflow edges with conditional routing - Simplified for performance
        workflow.set_entry_point("route_entry")
        print("[WORKFLOW] 🎯 Entry point set to: route_entry (HARDCODED ROUTING)")
        
        # Add entry routing node
        workflow.add_conditional_edges(
            "route_entry",
            self._route_from_entry,
            {
                "requirements": "analyze_requirements",
                "architecture": "design_architecture", 
                "development": "develop_solution",
                "testing": "test_solution",
                "deployment": "plan_deployment",
                "management": "manage_project",
                "security": "security_review",
                "collaboration": "collaborate",
                "end": END
            }
        )

        workflow.add_conditional_edges(
            "analyze_requirements",
            self._route_next_step,
            {
                "architecture": "design_architecture",
                "development": "develop_solution", 
                "testing": "test_solution",
                "deployment": "plan_deployment",
                "management": "manage_project",
                "security": "security_review",
                "collaboration": "collaborate",
                "end": END
            }
        )

        # All other nodes route to collaboration or end
        for node in ["design_architecture", "develop_solution", "test_solution", "plan_deployment", "manage_project", "security_review"]:
            workflow.add_edge(node, END)

        workflow.add_edge("collaborate", END)

        print("[WORKFLOW] Created new workflow graph with route_entry as entry point")
        return workflow.compile()

    async def _analyze_requirements(self, state: SDLCState) -> SDLCState:
        agent = self.agents["requirements_analyst"]
        context = state["project_context"].copy()
        context["uploaded_files"] = state.get("uploaded_files", [])
        
        # Add context about being directly called
        if state.get("called_agent") == "requirements_analyst":
            context["direct_call"] = True
            context["interaction_type"] = "You were directly addressed by the user. Respond as if you are having a direct conversation with them."
        
        response = await agent.process_request(state["user_request"], context)
        state["agent_outputs"]["requirements_analyst"] = response
        state["current_phase"] = "requirements_analysis"
        return state

    async def _design_architecture(self, state: SDLCState) -> SDLCState:
        agent = self.agents["software_architect"]
        context = state["project_context"].copy()
        context["uploaded_files"] = state.get("uploaded_files", [])
        
        if state.get("called_agent") == "software_architect":
            context["direct_call"] = True
            context["interaction_type"] = "You were directly addressed by the user. Respond as if you are having a direct conversation with them."
        
        response = await agent.process_request(state["user_request"], context)
        state["agent_outputs"]["software_architect"] = response
        state["current_phase"] = "architecture_design"
        return state

    async def _develop_solution(self, state: SDLCState) -> SDLCState:
        agent = self.agents["developer"]
        context = state["project_context"].copy()
        context["uploaded_files"] = state.get("uploaded_files", [])
        
        if state.get("called_agent") == "developer":
            context["direct_call"] = True
            context["interaction_type"] = "You were directly addressed by the user. Respond as if you are having a direct conversation with them."
        
        response = await agent.process_request(state["user_request"], context)
        state["agent_outputs"]["developer"] = response
        state["current_phase"] = "development"
        return state

    async def _test_solution(self, state: SDLCState) -> SDLCState:
        agent = self.agents["qa_tester"]
        context = state["project_context"].copy()
        context["uploaded_files"] = state.get("uploaded_files", [])
        
        if state.get("called_agent") == "qa_tester":
            context["direct_call"] = True
            context["interaction_type"] = "You were directly addressed by the user. Respond as if you are having a direct conversation with them."
        
        response = await agent.process_request(state["user_request"], context)
        state["agent_outputs"]["qa_tester"] = response
        state["current_phase"] = "testing"
        return state

    async def _plan_deployment(self, state: SDLCState) -> SDLCState:
        agent = self.agents["devops_engineer"]
        context = state["project_context"].copy()
        context["uploaded_files"] = state.get("uploaded_files", [])
        
        if state.get("called_agent") == "devops_engineer":
            context["direct_call"] = True
            context["interaction_type"] = "You were directly addressed by the user. Respond as if you are having a direct conversation with them."
        
        response = await agent.process_request(state["user_request"], context)
        state["agent_outputs"]["devops_engineer"] = response
        state["current_phase"] = "deployment_planning"
        return state

    async def _manage_project(self, state: SDLCState) -> SDLCState:
        agent = self.agents["project_manager"]
        context = state["project_context"].copy()
        context["uploaded_files"] = state.get("uploaded_files", [])
        
        if state.get("called_agent") == "project_manager":
            context["direct_call"] = True
            context["interaction_type"] = "You were directly addressed by the user. Respond as if you are having a direct conversation with them."
        
        response = await agent.process_request(state["user_request"], context)
        state["agent_outputs"]["project_manager"] = response
        state["current_phase"] = "project_management"
        return state

    async def _security_review(self, state: SDLCState) -> SDLCState:
        agent = self.agents["security_expert"]
        context = state["project_context"].copy()
        context["uploaded_files"] = state.get("uploaded_files", [])
        
        if state.get("called_agent") == "security_expert":
            context["direct_call"] = True
            context["interaction_type"] = "You were directly addressed by the user. Respond as if you are having a direct conversation with them."
        
        response = await agent.process_request(state["user_request"], context)
        state["agent_outputs"]["security_expert"] = response
        state["current_phase"] = "security_review"
        return state

    async def _multi_agent_collaboration(self, state: SDLCState) -> SDLCState:
        """Handle multi-agent collaboration with automatic agent-to-agent communication"""
        
        # CRITICAL: If called_agent is set, this is a DIRECT CALL - skip collaboration!
        called_agent = state.get("called_agent")
        if called_agent:
            print(f"[COLLAB] Direct call to {called_agent} detected - executing ONLY that agent, no collaboration")
            # Execute only the called agent
            agent = self.agents.get(called_agent)
            if agent:
                context = state["project_context"].copy()
                context["uploaded_files"] = state.get("uploaded_files", [])
                context["direct_call"] = True
                context["interaction_type"] = "You were directly addressed by the user. Respond naturally as if having a one-on-one conversation."
                
                response = await agent.process_request(state["user_request"], context)
                state["agent_outputs"][called_agent] = response
                print(f"[COLLAB] Executed direct call to {called_agent}, response length: {len(response)}")
            else:
                print(f"[COLLAB] ERROR: Called agent {called_agent} not found!")
            return state
        
        requested_agents = state.get("requested_agents", [])
        
        print(f"[COLLAB] Requested agents: {requested_agents}")
        print(f"[COLLAB] This should NOT run for direct calls - called_agent was: {state.get('called_agent')}")
        
        if not requested_agents:
            # Only fall back to content-based routing if no agents specified AND no direct call
            request = state["user_request"].lower()
            if any(word in request for word in ["requirements", "requirement", "spec", "user story"]):
                requested_agents = ["requirements_analyst"]
            elif any(word in request for word in ["architecture", "design", "system"]):
                requested_agents = ["software_architect"]
            elif any(word in request for word in ["code", "implement", "develop", "build"]):
                requested_agents = ["developer"]
            elif any(word in request for word in ["test", "testing", "quality", "qa"]):
                requested_agents = ["qa_tester"]
            elif any(word in request for word in ["deploy", "deployment", "infrastructure"]):
                requested_agents = ["devops_engineer"]
            elif any(word in request for word in ["project", "planning", "manage"]):
                requested_agents = ["project_manager"]
            elif any(word in request for word in ["security", "secure", "vulnerability"]):
                requested_agents = ["security_expert"]
            else:
                # NO DEFAULT - let the user choose
                print(f"[COLLAB] No specific domain detected, no agents to activate")
                return state
        
        print(f"[COLLAB] Final collaboration list: {requested_agents}")
        
        # Skip A2A detection if this is a direct single-agent call
        if called_agent and len(requested_agents) == 1:
            print(f"[COLLAB] Direct single-agent call - skipping A2A mention detection")
            all_agents = requested_agents
            is_exclusive_request = False
        else:
            # Check if any previous agent responses mention other agents by name
            previous_responses = state.get("agent_outputs", {})
            mentioned_agents = set()
            is_exclusive_request = False
            
            # Agent name mappings for A2A communication - Enhanced with more variations
            agent_name_mapping = {
                "sarah": "requirements_analyst",
                "sarah chen": "requirements_analyst", 
                "alex": "developer",
                "alex kim": "developer",
                "marcus": "software_architect", 
                "marcus rodriguez": "software_architect",
                "jessica": "qa_tester",
                "jessica wu": "qa_tester",
                "david": "devops_engineer",
                "david singh": "devops_engineer", 
                "emily": "project_manager",
                "emily johnson": "project_manager",
                "robert": "security_expert",
                "robert chen": "security_expert",
                # Additional patterns for better detection
                "requirements": "requirements_analyst",
                "architect": "software_architect",
                "developer": "developer",
                "tester": "qa_tester", 
                "qa": "qa_tester",
                "devops": "devops_engineer",
                "manager": "project_manager",
                "security": "security_expert"
            }
            
            # Check for agent mentions in previous responses AND user request
            user_request_lower = state["user_request"].lower()
            print(f"[A2A] Checking user request for direct agent mentions and dismissals...")
            
            # Detect agent dismissals/drop-offs
            dismissal_patterns = ["drop off", "drop out", "leave", "dismiss", "step back", "thank you", "thanks", "goodbye", "bye"]
            agent_dismissals = set()
            
            for name, agent_key in agent_name_mapping.items():
                # Check if agent is being dismissed
                for dismissal in dismissal_patterns:
                    if f"{name}" in user_request_lower and dismissal in user_request_lower:
                        agent_dismissals.add(agent_key)
                        print(f"[A2A] User dismissing '{name}' -> removing {agent_key}")
            
            # Detect agent mentions (excluding dismissed ones)
            for name, agent_key in agent_name_mapping.items():
                if name in user_request_lower and agent_key not in requested_agents and agent_key not in agent_dismissals:
                    mentioned_agents.add(agent_key)
                    print(f"[A2A] User mentioned '{name}' -> adding {agent_key}")
            
            # Handle continuation patterns ("continue with", "chat with", "work with")
            continuation_patterns = [
                "continue", "chat with", "work with", "speak with", "talk to", 
                "call", "bring in", "would like to talk to", "want to talk to",
                "need to talk to", "like to speak to", "want to speak to"
            ]
            if any(pattern in user_request_lower for pattern in continuation_patterns):
                print(f"[A2A] Continuation pattern detected - focusing on specific agents")
                # If user says "I would like to talk to Marc", only include Marc
                for name, agent_key in agent_name_mapping.items():
                    if any(f"{pattern} {name}" in user_request_lower for pattern in continuation_patterns):
                        # This is an EXCLUSIVE request - clear other agents
                        mentioned_agents = {agent_key}
                        requested_agents = [agent_key]
                        print(f"[A2A] Exclusive request to talk to {name} -> using ONLY {agent_key}")
                        break
            
            # Apply dismissals - remove dismissed agents from previous responses tracking
            if agent_dismissals and "agent_outputs" in state:
                print(f"[A2A] Removing dismissed agents from active conversation: {agent_dismissals}")
                for dismissed_agent in agent_dismissals:
                    if dismissed_agent in state["agent_outputs"]:
                        del state["agent_outputs"][dismissed_agent]
            
            # Handle exclusive talk-to requests - remove all other agents
            exclusive_patterns = ["would like to talk to", "want to talk to", "need to talk to", 
                                 "like to speak to", "want to speak to", "would like to speak to"]
            is_exclusive_request = False
            for pattern in exclusive_patterns:
                if pattern in user_request_lower:
                    is_exclusive_request = True
                    print(f"[A2A] Exclusive request detected: '{pattern}'")
                    # Clear all previous agent outputs except the requested one
                    if mentioned_agents and "agent_outputs" in state:
                        agents_to_remove = [a for a in state["agent_outputs"].keys() if a not in mentioned_agents]
                        for agent_to_remove in agents_to_remove:
                            del state["agent_outputs"][agent_to_remove]
                            print(f"[A2A] Removed {agent_to_remove} from conversation (exclusive request)")
                    break
            
            # SECOND: Check previous agent responses for mentions (only if not a direct call)
            if not called_agent:
                for agent_id, response in previous_responses.items():
                    if isinstance(response, str):
                        response_lower = response.lower()
                        print(f"[A2A] Checking {agent_id} response for mentions...")
                        
                        for name, agent_key in agent_name_mapping.items():
                            if name in response_lower and agent_key not in requested_agents:
                                mentioned_agents.add(agent_key)
                                print(f"[A2A] {agent_id} mentioned '{name}' -> adding {agent_key}")
                                
                        # Additional check for names mentioned together (e.g., "Alex, Jessica, David, Emily, and Robert")
                        if len(mentioned_agents) < 3:  # If we haven't found many mentions, try a broader search
                            all_names = ["alex", "jessica", "david", "emily", "robert", "kim", "wu", "singh", "johnson", "chen"]
                            found_names = [name for name in all_names if name in response_lower]
                            if len(found_names) >= 2:  # Multiple names mentioned together
                                print(f"[A2A] Multiple names detected in {agent_id} response: {found_names}")
                                # Add all remaining agents when multiple names are mentioned
                                for agent_key in ["developer", "qa_tester", "devops_engineer", "project_manager", "security_expert"]:
                                    if agent_key not in requested_agents:
                                        mentioned_agents.add(agent_key)
                                        print(f"[A2A] Multi-name trigger -> adding {agent_key}")
                    else:
                        print(f"[A2A] Warning: Response from {agent_id} is not a string: {type(response)}")
            
            # Add mentioned agents to the collaboration
            # For exclusive requests, use ONLY the mentioned agents
            if is_exclusive_request and mentioned_agents:
                all_agents = list(mentioned_agents)
                print(f"[WORKFLOW] Exclusive request - using ONLY: {all_agents}")
            else:
                all_agents = list(set(requested_agents + list(mentioned_agents)))
                print(f"[WORKFLOW] Final agent list (including A2A): {all_agents}")
        
        collaboration_tasks = []
        for agent_name in all_agents:
            if agent_name in self.agents:
                print(f"[WORKFLOW] Adding task for {agent_name}")
                try:
                    agent = self.agents[agent_name]
                    
                    # Build context from previous agent responses
                    collaboration_context = state["project_context"].copy()
                    collaboration_context["uploaded_files"] = state.get("uploaded_files", [])
                    if previous_responses:
                        collaboration_context["previous_responses"] = previous_responses
                        collaboration_context["conversation_flow"] = "This is part of an ongoing multi-agent collaboration. Please respond to the user's request and any relevant points raised by other team members."
                    
                    task = agent.process_request(state["user_request"], collaboration_context)
                    collaboration_tasks.append((agent_name, task))
                except Exception as agent_error:
                    print(f"[WORKFLOW] Error creating task for {agent_name}: {agent_error}")
            else:
                print(f"[WORKFLOW] Warning: Agent {agent_name} not found in available agents")

        # Execute agents in parallel
        if collaboration_tasks:
            print(f"[WORKFLOW] Executing {len(collaboration_tasks)} agent tasks")
            results = await asyncio.gather(*[task for _, task in collaboration_tasks])
            for (agent_name, _), result in zip(collaboration_tasks, results):
                print(f"[WORKFLOW] Got result from {agent_name}: {len(result)} chars")
                state["agent_outputs"][agent_name] = result
        else:
            print("[WORKFLOW] No collaboration tasks to execute")

        return state

    def _route_entry_point(self, state: SDLCState) -> SDLCState:
        """Entry point that just passes through state for routing"""
        print("="*80)
        print("[WORKFLOW] 🔥 NUCLEAR ENTRY POINT ACTIVATED!")
        print(f"[WORKFLOW] 📝 Message: '{state.get('user_request')}'")
        print(f"[WORKFLOW] 👥 Requested agents: {state.get('requested_agents', [])}")
        print(f"[WORKFLOW] 🎯 This is the HARDCODED routing version!")
        print("="*80)
        return state
    
    def _route_from_entry(self, state: SDLCState) -> str:
        """Route from entry point based on requested agents or request content"""
        requested_agents = state.get("requested_agents", [])
        raw_request = state["user_request"]
        if isinstance(raw_request, str):
            user_request_lower = raw_request.strip().lower()
        else:
            user_request_lower = str(raw_request).strip().lower()

        # Always clear any previous direct-call marker before evaluating this turn
        state["called_agent"] = None

        print(f"\n" + "="*80)
        print(f"[ROUTE] 🔍 NEW REQUEST RECEIVED")
        print(f"[ROUTE] 📝 Message: '{state['user_request']}'")
        print(f"[ROUTE] 👥 Requested agents from UI: {requested_agents}")
        print(f"[ROUTE] 🎯 called_agent (before routing): {state.get('called_agent')}")
        print("="*80)
        
        # COMPLETE HARDCODED AGENT ROUTING - REPLACES ALL COMPLEX LOGIC
        print(f"[ROUTE] 🧪 HARDCODED ROUTING: Checking for agent names...")
        
        # Check all agent names with proper logging
        agent_mappings = {
            "dave": ("deployment", "devops_engineer", "Dave (DevOps Engineer)"),
            "marc": ("architecture", "software_architect", "Marc (Software Architect)"), 
            "alex": ("development", "developer", "Alex (Developer)"),
            "jess": ("testing", "qa_tester", "Jess (QA Tester)"),
            "emma": ("management", "project_manager", "Emma (Project Manager)"),
            "robt": ("security", "security_expert", "Robt (Security Expert)"),
            "rob": ("security", "security_expert", "Rob (Security Expert)"),
            "sara": ("requirements", "requirements_analyst", "Sara (Requirements Analyst)")
        }
        
        # Check each agent name
        for name, (route, agent_id, display_name) in agent_mappings.items():
            if name in user_request_lower:
                print(f"[ROUTE] ✅ HARDCODED: Found '{name}' → routing to {route}")
                print(f"[ROUTE] 🎯 Setting called_agent to: {agent_id}")
                print(f"[ROUTE] 👤 Agent: {display_name}")
                state["called_agent"] = agent_id
                return route
        
        # Check for team greetings
        if any(word in user_request_lower for word in ["everyone", "everybody", "team", "all"]):
            print("[ROUTE] 👥 TEAM GREETING DETECTED: Activating collaboration mode")
            return "collaboration"
        
        # No match found - end workflow (DO NOT default to Sara!)
        print(f"[ROUTE] ⚠️  NO AGENT DETECTED in: '{user_request_lower}'")
        print("[ROUTE] Available: dave, marc, alex, jess, emma, robt, sara")
        print("[ROUTE] 🛑 ENDING WORKFLOW - No default to Sara!")
        return "end"

        # Enhanced agent name detection patterns
        agent_patterns = {
            "sarah": ("requirements", "requirements_analyst"),
            "sara": ("requirements", "requirements_analyst"),
            "marcus": ("architecture", "software_architect"),
            "marc": ("architecture", "software_architect"),
            "alex": ("development", "developer"),
            "alexander": ("development", "developer"),
            "jessica": ("testing", "qa_tester"),
            "jess": ("testing", "qa_tester"),
            "david": ("deployment", "devops_engineer"),
            "dave": ("deployment", "devops_engineer"),
            "emily": ("management", "project_manager"),
            "emma": ("management", "project_manager"),
            "robert": ("security", "security_expert"),
            "robt": ("security", "security_expert"),
            "rob": ("security", "security_expert")
        }

        def _activate_agent(name_key: str) -> Optional[str]:
            if name_key in agent_patterns:
                route, agent_id = agent_patterns[name_key]
                print(f"[ROUTE] Direct reference to {name_key} detected, routing to {route}")
                state["called_agent"] = agent_id
                # Ensure the directly addressed agent is treated as the requested target
                if not requested_agents:
                    state["requested_agents"] = [agent_id]
                elif agent_id not in state["requested_agents"]:
                    state["requested_agents"].insert(0, agent_id)
                return route
            return None

        # PRIORITY 1: Team greetings ("Hi Everyone", "Hello Team", "Hi All", etc.)
        team_greeting_patterns = [
            r"^(hi|hello|hey|greetings|good morning|good afternoon)\s+(everyone|everybody|team|all|all agents|folks|guys)",
            r"^(hi|hello|hey|greetings)\s+there\s+(everyone|team|all)"
        ]
        for pattern in team_greeting_patterns:
            if re.search(pattern, user_request_lower):
                print("[ROUTE] 👥 TEAM GREETING DETECTED: Activating collaboration mode")
                print("[ROUTE] All agents will be available to respond")
                print("[ROUTE] 🚀 RETURNING ROUTE: 'collaboration'")
                print("="*80 + "\n")
                return "collaboration"

        # PRIORITY 2: Direct agent greetings ("Hi Marc", "Hello Jess!", etc.)
        greeting_match = re.match(
            r"^(hi|hello|hey|greetings|good morning|good afternoon|yo)[\s,@]+([a-z .'-]+)",
            user_request_lower
        )
        if greeting_match:
            raw_name = greeting_match.group(2).strip()
            cleaned_name = re.split(r"[\s,!.?:;]+", raw_name)[0].strip("'\"-_")
            
            # Check if it's a team reference that slipped through
            if cleaned_name in ['everyone', 'everybody', 'team', 'all', 'folks', 'guys']:
                print("[ROUTE] 👥 TEAM REFERENCE DETECTED: Activating collaboration mode")
                print("[ROUTE] 🚀 RETURNING ROUTE: 'collaboration'")
                print("="*80 + "\n")
                return "collaboration"
            
            route = _activate_agent(cleaned_name)
            if route:
                print(f"[ROUTE] ✅ DIRECT GREETING DETECTED: '{greeting_match.group(0)}' → {cleaned_name} → {route}")
                print(f"[ROUTE] 🎯 called_agent set to: {state.get('called_agent')}")
                print(f"[ROUTE] 📋 This is a DIRECT CALL - only this agent will respond")
                print(f"[ROUTE] 🚀 RETURNING ROUTE: '{route}'")
                print("="*80 + "\n")
                return route
            else:
                print(f"[ROUTE] ⚠️  Greeting detected but agent name '{cleaned_name}' not recognized")
                print(f"[ROUTE] Available agents: {list(agent_patterns.keys())}")

        # PRIORITY 2: Direct single-word agent calls ("Marc", "@alex", "marcus:")
        direct_name_match = re.match(r"^@?([a-z]+)[\s,!.?:;-]*$", user_request_lower)
        if direct_name_match:
            name_key = direct_name_match.group(1)
            route = _activate_agent(name_key)
            if route:
                return route

        # PRIORITY 3: Agent name appears at the start followed by punctuation ("Alex, can you...")
        words = user_request_lower.split()
        if words:
            first_token = re.sub(r"[^a-z]", "", words[0])
            route = _activate_agent(first_token)
            if route:
                return route

        # PRIORITY 4: Check for multiple agent mentions throughout the text
        mentioned_agents = []
        for name, (route, agent_id) in agent_patterns.items():
            pattern = rf"\b{name}\b"
            if re.search(pattern, user_request_lower):
                mentioned_agents.append((name, route, agent_id))

        print(f"[ROUTE] Mentioned agents: {[name for name, _, _ in mentioned_agents]}")

        if len(mentioned_agents) > 1:
            print("[ROUTE] Multiple agent mentions detected, routing to collaboration")
            return "collaboration"
        elif len(mentioned_agents) == 1:
            name, route, agent_id = mentioned_agents[0]
            # Direct agent mention - route to that agent only
            # NOTE: Collaboration keywords are ONLY checked in team greetings (PRIORITY 1)
            # Don't check for "team" or "everyone" here - user might be asking ABOUT the team
            print(f"[ROUTE] Single agent mention '{name}' in context, routing to {route}")
            state["called_agent"] = agent_id
            return route

        # Priority 5: If multiple agents are explicitly requested via UI, go to collaboration
        if len(requested_agents) > 1:
            print(f"[ROUTE] Multiple agents requested via UI ({len(requested_agents)}), routing to collaboration")
            return "collaboration"
        elif len(requested_agents) == 1:
            # Single agent request - route directly to that agent
            # User explicitly selected ONE agent, don't override with collaboration
            agent = requested_agents[0]
            print(f"[ROUTE] Single agent requested via UI: {agent}")
            state["called_agent"] = agent
            if agent == "requirements_analyst":
                return "requirements"
            elif agent == "software_architect":
                return "architecture"
            elif agent == "developer":
                return "development"
            elif agent == "qa_tester":
                return "testing"
            elif agent == "devops_engineer":
                return "deployment"
            elif agent == "project_manager":
                return "management"
            elif agent == "security_expert":
                return "security"

        # Priority 6: Route based on request content (fallback - only when no agents mentioned)
        request = state["user_request"].lower()
        if any(word in request for word in ["architecture", "design", "system", "structure"]):
            return "architecture"
        elif any(word in request for word in ["code", "implement", "develop", "build"]):
            return "development"
        elif any(word in request for word in ["test", "testing", "quality", "qa"]):
            return "testing"
        elif any(word in request for word in ["deploy", "deployment", "infrastructure", "devops"]):
            return "deployment"
        elif any(word in request for word in ["project", "planning", "manage", "timeline"]):
            return "management"
        elif any(word in request for word in ["security", "secure", "vulnerability"]):
            return "security"
        else:
            # NO DEFAULT - if greeting detection failed, don't activate any agent
            print("[ROUTE] ⚠️  No agent or domain detected - ending workflow")
            print("[ROUTE] Message was:", state["user_request"])
            return "end"

    def _route_next_step(self, state: SDLCState) -> str:
        # Priority 1: If specific agents are requested, use collaboration
        requested_agents = state.get("requested_agents", [])
        if len(requested_agents) >= 1:
            # Always use collaboration for agent requests
            return "collaboration"
        
        # Priority 2: Route based on request content
        request = state["user_request"].lower()
        if any(word in request for word in ["architecture", "design", "system", "structure"]):
            return "architecture"
        elif any(word in request for word in ["code", "implement", "develop", "build"]):
            return "development"
        else:
            return "collaboration"  # Default to collaboration

    def _route_after_architecture(self, state: SDLCState) -> str:
        request = state["user_request"].lower()

        if any(word in request for word in ["security", "secure", "vulnerability"]):
            return "security"
        elif any(word in request for word in ["code", "implement", "develop"]):
            return "development"
        elif len(state.get("requested_agents", [])) > 1:
            return "collaboration"
        else:
            return "end"

    def _route_after_development(self, state: SDLCState) -> str:
        request = state["user_request"].lower()

        if any(word in request for word in ["test", "testing", "qa", "quality"]):
            return "testing"
        elif any(word in request for word in ["security", "secure"]):
            return "security"
        elif len(state.get("requested_agents", [])) > 1:
            return "collaboration"
        else:
            return "end"

    def _route_after_testing(self, state: SDLCState) -> str:
        request = state["user_request"].lower()

        if any(word in request for word in ["deploy", "deployment", "production"]):
            return "deployment"
        elif any(word in request for word in ["fix", "bug", "issue"]):
            return "development"
        elif len(state.get("requested_agents", [])) > 1:
            return "collaboration"
        else:
            return "end"

    def _route_after_deployment(self, state: SDLCState) -> str:
        if len(state.get("requested_agents", [])) > 1:
            return "collaboration"
        else:
            return "management"

    def _route_after_security(self, state: SDLCState) -> str:
        request = state["user_request"].lower()

        if any(word in request for word in ["fix", "implement", "code"]):
            return "development"
        elif any(word in request for word in ["test", "testing"]):
            return "testing"
        elif len(state.get("requested_agents", [])) > 1:
            return "collaboration"
        else:
            return "end"

    def _route_after_management(self, state: SDLCState) -> str:
        if len(state.get("requested_agents", [])) > 1:
            return "collaboration"
        else:
            return "end"