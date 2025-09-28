# workflows/sdlc_workflow.py
from langgraph.graph import StateGraph, END
from typing import TypedDict, List
import asyncio

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
        response = await agent.process_request(state["user_request"], context)

        state["agent_outputs"]["requirements_analyst"] = response
        state["current_phase"] = "requirements_analysis"

        return state

    async def _design_architecture(self, state: SDLCState) -> SDLCState:
        agent = self.agents["software_architect"]
        context = state["project_context"].copy()
        context["uploaded_files"] = state.get("uploaded_files", [])
        response = await agent.process_request(state["user_request"], context)

        state["agent_outputs"]["software_architect"] = response
        state["current_phase"] = "architecture_design"

        return state

    async def _develop_solution(self, state: SDLCState) -> SDLCState:
        agent = self.agents["developer"]
        context = state["project_context"].copy()
        context["uploaded_files"] = state.get("uploaded_files", [])
        response = await agent.process_request(state["user_request"], context)

        state["agent_outputs"]["developer"] = response
        state["current_phase"] = "development"

        return state

    async def _test_solution(self, state: SDLCState) -> SDLCState:
        agent = self.agents["qa_tester"]
        context = state["project_context"].copy()
        context["uploaded_files"] = state.get("uploaded_files", [])
        response = await agent.process_request(state["user_request"], context)

        state["agent_outputs"]["qa_tester"] = response
        state["current_phase"] = "testing"

        return state

    async def _plan_deployment(self, state: SDLCState) -> SDLCState:
        agent = self.agents["devops_engineer"]
        context = state["project_context"].copy()
        context["uploaded_files"] = state.get("uploaded_files", [])
        response = await agent.process_request(state["user_request"], context)

        state["agent_outputs"]["devops_engineer"] = response
        state["current_phase"] = "deployment_planning"

        return state

    async def _manage_project(self, state: SDLCState) -> SDLCState:
        agent = self.agents["project_manager"]
        context = state["project_context"].copy()
        context["uploaded_files"] = state.get("uploaded_files", [])
        response = await agent.process_request(state["user_request"], context)

        state["agent_outputs"]["project_manager"] = response
        state["current_phase"] = "project_management"

        return state

    async def _security_review(self, state: SDLCState) -> SDLCState:
        agent = self.agents["security_expert"]
        context = state["project_context"].copy()
        context["uploaded_files"] = state.get("uploaded_files", [])
        response = await agent.process_request(state["user_request"], context)

        state["agent_outputs"]["security_expert"] = response
        state["current_phase"] = "security_review"

        return state

    async def _multi_agent_collaboration(self, state: SDLCState) -> SDLCState:
        """Handle multi-agent collaboration with automatic agent-to-agent communication"""
        requested_agents = state.get("requested_agents", [])
        
        # Debug: Print what agents were actually requested
        print(f"[COLLAB] Original requested_agents: {requested_agents}")
        
        if not requested_agents:
            # Fallback: determine agent based on request content
            request = state["user_request"].lower()
            if any(word in request for word in ["requirements", "requirement", "spec", "user story"]):
                requested_agents = ["requirements_analyst"]
            elif any(word in request for word in ["architecture", "design", "system"]):
                requested_agents = ["software_architect"]
            else:
                requested_agents = ["requirements_analyst"]  # Default
            print(f"[COLLAB] No agents requested, using fallback: {requested_agents}")
        
        print(f"[WORKFLOW] Collaboration with agents: {requested_agents}")
        
        # Check if any previous agent responses mention other agents by name
        previous_responses = state.get("agent_outputs", {})
        mentioned_agents = set()
        
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
        mentioned_agents = set()
        
        # FIRST: Check the user's request for direct agent mentions AND dismissals
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
        continuation_patterns = ["continue", "chat with", "work with", "speak with", "talk to"]
        if any(pattern in user_request_lower for pattern in continuation_patterns):
            print(f"[A2A] Continuation pattern detected - focusing on specific agents")
            # If user says "continue with Marcus", only include Marcus and dismiss others
            for name, agent_key in agent_name_mapping.items():
                if any(f"{pattern} {name}" in user_request_lower for pattern in continuation_patterns):
                    mentioned_agents.add(agent_key)
                    print(f"[A2A] Continuing conversation with {name} -> adding {agent_key}")
        
        # IMPORTANT: For direct single agent calls (like "Hi Alex"), only include that agent
        single_agent_patterns = ["hi ", "hello ", "hey "]
        is_single_direct_call = False
        for pattern in single_agent_patterns:
            for name, agent_key in agent_name_mapping.items():
                if f"{pattern}{name}" in user_request_lower and len(mentioned_agents) == 1:
                    is_single_direct_call = True
                    print(f"[A2A] Direct single agent call detected: {pattern}{name}")
                    # Clear any other agents and only include the directly called agent
                    mentioned_agents = {agent_key}
                    break
            if is_single_direct_call:
                break
        
        # Apply dismissals - remove dismissed agents from previous responses tracking
        if agent_dismissals and "agent_outputs" in state:
            print(f"[A2A] Removing dismissed agents from active conversation: {agent_dismissals}")
            for dismissed_agent in agent_dismissals:
                if dismissed_agent in state["agent_outputs"]:
                    del state["agent_outputs"][dismissed_agent]
        
        # SECOND: Check previous agent responses for mentions
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
        print(f"[WORKFLOW] Entry point - requested agents: {state.get('requested_agents', [])}")
        return state
    
    def _route_from_entry(self, state: SDLCState) -> str:
        """Route from entry point based on requested agents or request content"""
        requested_agents = state.get("requested_agents", [])
        
        # Check if user mentioned agents by name in their request
        user_request_lower = state["user_request"].lower()
        agent_name_mentions = ["sarah", "marcus", "alex", "jessica", "david", "emily", "robert"]
        
        # PRIORITY 1: Single direct agent greetings - handle these first and route to specific agent
        greeting_patterns = ["hi ", "hello ", "hey ", "greetings ", "good morning ", "good afternoon "]
        for pattern in greeting_patterns:
            if user_request_lower.startswith(pattern):
                # Extract the name after the greeting
                remaining = user_request_lower[len(pattern):].strip()
                
                # Map greeting directly to agent workflow (NOT collaboration)
                if remaining.startswith("sarah"):
                    print(f"[ROUTE] Direct greeting to Sarah detected, routing to requirements")
                    return "requirements"
                elif remaining.startswith("alex"):
                    print(f"[ROUTE] Direct greeting to Alex detected, routing to development") 
                    return "development"
                elif remaining.startswith("marcus"):
                    print(f"[ROUTE] Direct greeting to Marcus detected, routing to architecture")
                    return "architecture"
                elif remaining.startswith("jessica"):
                    print(f"[ROUTE] Direct greeting to Jessica detected, routing to testing")
                    return "testing"
                elif remaining.startswith("david"):
                    print(f"[ROUTE] Direct greeting to David detected, routing to deployment")
                    return "deployment"
                elif remaining.startswith("emily"):
                    print(f"[ROUTE] Direct greeting to Emily detected, routing to management")
                    return "management"
                elif remaining.startswith("robert"):
                    print(f"[ROUTE] Direct greeting to Robert detected, routing to security")
                    return "security"
        
        # Count all agent mentions for other routing logic
        mentioned_count = sum(1 for name in agent_name_mentions if name in user_request_lower)
        print(f"[ROUTE] User mentioned {mentioned_count} agent names in request")
        
        # Priority 2: Multiple agent mentions or collaboration requests
        if mentioned_count > 1:
            print(f"[ROUTE] Multiple agent mentions detected ({mentioned_count} agents), routing to collaboration")
            return "collaboration"
        elif mentioned_count == 1:
            # Single agent mention but not a direct greeting - check if it's collaboration context
            request = state["user_request"].lower()
            collab_keywords = ["introduce", "introduction", "team", "everyone", "all agents", "hello team", "work with", "collaborate"]
            if any(keyword in request for keyword in collab_keywords):
                print(f"[ROUTE] Single agent mention with collaboration keywords, routing to collaboration")
                return "collaboration"
            else:
                # Single agent mention in context - route directly to their workflow
                if "sarah" in user_request_lower:
                    return "requirements"
                elif "alex" in user_request_lower:
                    return "development"
                elif "marcus" in user_request_lower:
                    return "architecture"
                elif "jessica" in user_request_lower:
                    return "testing"
                elif "david" in user_request_lower:
                    return "deployment"
                elif "emily" in user_request_lower:
                    return "management"
                elif "robert" in user_request_lower:
                    return "security"
        
        # Priority 3: If multiple agents are explicitly requested via UI, go to collaboration  
        if len(requested_agents) > 1:
            print(f"[ROUTE] Multiple agents requested via UI ({len(requested_agents)}), routing to collaboration")
            return "collaboration"
        elif len(requested_agents) == 1:
            # Single agent request - check if it's a collaboration request by content
            request = state["user_request"].lower()
            collab_keywords = ["introduce", "introduction", "team", "everyone", "all agents", "hello team"]
            if any(keyword in request for keyword in collab_keywords):
                print(f"[ROUTE] Collaboration keywords detected, routing to collaboration")
                return "collaboration"
            
            # Route to specific agent workflow for single agent requests
            agent = requested_agents[0]
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
        
        # Priority 4: Route based on request content (fallback - only when no agents mentioned)
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
            # Only default to requirements if no specific agent or domain is mentioned
            return "requirements"

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