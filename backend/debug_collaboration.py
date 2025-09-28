#!/usr/bin/env python3
"""
Debug the collaboration workflow directly
"""

import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from workflows.sdlc_workflow import SDLCWorkflow

async def debug_collaboration():
    print("=== Debugging Multi-Agent Collaboration ===")
    
    workflow = SDLCWorkflow()
    
    # Test with all 7 agents requested
    test_state = {
        "user_request": "Hello team! Please introduce yourselves - Sarah, Marcus, Alex, Jessica, David, Emily, and Robert. I want to hear from everyone.",
        "current_phase": "initial",
        "agent_outputs": {},
        "conversation_history": [],
        "project_context": {
            "projectName": "TeamIntroduction",
            "technology": "", 
            "phase": "planning"
        },
        "next_agent": "",
        "final_response": "",
        "requested_agents": [
            "requirements_analyst",
            "software_architect", 
            "developer",
            "qa_tester",
            "devops_engineer",
            "project_manager",
            "security_expert"
        ]
    }
    
    print(f"Initial requested agents: {test_state['requested_agents']}")
    print(f"Total requested: {len(test_state['requested_agents'])}")
    
    # Test the entry point routing
    entry_result = workflow._route_entry_point(test_state)
    route_decision = workflow._route_from_entry(entry_result)
    print(f"Route decision: {route_decision}")
    
    if route_decision == "collaboration":
        print("\n=== Testing Direct Collaboration ===")
        result = await workflow._multi_agent_collaboration(test_state)
        
        print(f"Collaboration result - agents who responded: {list(result['agent_outputs'].keys())}")
        print(f"Total responses: {len(result['agent_outputs'])}")
        
        for agent, response in result['agent_outputs'].items():
            print(f"  {agent}: {len(response)} chars - {response[:100]}...")
        
        expected = {"requirements_analyst", "software_architect", "developer", "qa_tester", "devops_engineer", "project_manager", "security_expert"}
        actual = set(result['agent_outputs'].keys())
        missing = expected - actual
        
        if missing:
            print(f"\n❌ Missing agents: {sorted(missing)}")
            return False
        else:
            print(f"\n✅ All 7 agents responded successfully!")
            return True
    else:
        print(f"❌ Wrong route decision: {route_decision}, expected 'collaboration'")
        return False

if __name__ == "__main__":
    success = asyncio.run(debug_collaboration())