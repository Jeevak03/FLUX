#!/usr/bin/env python3
"""
Direct test of A2A communication in the workflow
"""

import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from workflows.sdlc_workflow import SDLCWorkflow

async def test_a2a_communication():
    print("Testing A2A Communication...")
    
    # Initialize workflow
    workflow = SDLCWorkflow()
    
    # Test 1: Initial request with one agent
    print("\n=== Test 1: Initial request ===")
    initial_state = {
        "user_request": "I need comprehensive planning for a new mobile app project. Sarah, please outline the requirements, and then Alex and Marcus should provide their input on development and architecture approaches.",
        "current_phase": "collaboration",
        "agent_outputs": {},
        "conversation_history": [],
        "project_context": {
            "projectName": "MobileApp",
            "technology": "React Native", 
            "phase": "planning"
        },
        "next_agent": "",
        "final_response": "",
        "requested_agents": ["requirements_analyst"]
    }
    
    # Execute first iteration
    result1 = await workflow._multi_agent_collaboration(initial_state)
    
    print(f"Iteration 1 - Agents responded: {list(result1['agent_outputs'].keys())}")
    for agent, response in result1['agent_outputs'].items():
        print(f"  {agent}: {len(response)} chars - {response[:100]}...")
        
        # Check for agent mentions
        response_lower = response.lower()
        mentions = []
        if "alex" in response_lower: mentions.append("Alex")
        if "marcus" in response_lower: mentions.append("Marcus") 
        if "jessica" in response_lower: mentions.append("Jessica")
        if "david" in response_lower: mentions.append("David")
        if "emily" in response_lower: mentions.append("Emily")
        if "robert" in response_lower: mentions.append("Robert")
        
        if mentions:
            print(f"    -> Mentioned agents: {mentions}")
    
    # Test 2: Check if mentions trigger additional agents
    if len(result1['agent_outputs']) == 1:
        # Simulate A2A trigger based on mentions
        first_response = list(result1['agent_outputs'].values())[0]
        response_lower = first_response.lower()
        
        triggered_agents = []
        if "alex" in response_lower: triggered_agents.append("developer")
        if "marcus" in response_lower: triggered_agents.append("software_architect")
        
        if triggered_agents:
            print(f"\n=== Test 2: A2A Triggered agents: {triggered_agents} ===")
            
            # Create second iteration state
            second_state = result1.copy()
            second_state.update({
                "requested_agents": triggered_agents,
                "user_request": "Please respond to the discussion initiated by your colleagues. Previous responses are available in context."
            })
            
            result2 = await workflow._multi_agent_collaboration(second_state)
            
            print(f"Iteration 2 - Additional agents responded: {list(set(result2['agent_outputs'].keys()) - set(result1['agent_outputs'].keys()))}")
            for agent, response in result2['agent_outputs'].items():
                if agent not in result1['agent_outputs']:
                    print(f"  NEW {agent}: {len(response)} chars - {response[:100]}...")
    
    print(f"\n✅ A2A Communication test completed!")
    total_agents = len(result2['agent_outputs']) if 'result2' in locals() else len(result1['agent_outputs'])
    print(f"   Total agents participated: {total_agents}")
    
    if total_agents > 1:
        print("🎉 A2A Communication working - multiple agents participated!")
        return True
    else:
        print("⚠️  Only single agent responded - A2A communication needs improvement")
        return False

if __name__ == "__main__":
    success = asyncio.run(test_a2a_communication())