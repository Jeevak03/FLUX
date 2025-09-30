#!/usr/bin/env python3
"""
Demo script to showcase Agent-to-Agent (A2A) Protocol capabilities
"""

import asyncio
import json
from workflows.sdlc_workflow import SDLCWorkflow, SDLCState

async def demo_a2a_protocol():
    """Demonstrate the A2A protocol with various scenarios"""
    
    print("=" * 60)
    print("🤖 FLUX A2A Protocol Demo")
    print("=" * 60)
    
    workflow = SDLCWorkflow()
    
    # Demo Scenario 1: Direct agent call
    print("\n📌 Scenario 1: Direct Agent Communication")
    print("-" * 40)
    
    state1 = SDLCState(
        user_request="Hi Alex, can you help me implement a user authentication system?",
        current_phase="initial",
        agent_outputs={},
        conversation_history=[],
        project_context={"project_name": "Demo App", "technology": "Python/FastAPI"},
        uploaded_files=[],
        next_agent="",
        final_response="",
        requested_agents=[],
        called_agent=""
    )
    
    print(f"User: {state1['user_request']}")
    result1 = await workflow.workflow.ainvoke(state1)
    
    for agent, response in result1.get("agent_outputs", {}).items():
        print(f"\n{agent.replace('_', ' ').title()}: {response[:200]}...")
    
    # Demo Scenario 2: Multi-agent collaboration triggered by A2A
    print("\n\n📌 Scenario 2: A2A Triggered Multi-Agent Collaboration")
    print("-" * 40)
    
    # Simulate a follow-up where Alex mentions other team members
    state2 = SDLCState(
        user_request="Great! Can you also get Jessica to review the security aspects and Dave to plan the deployment?",
        current_phase="collaboration",
        agent_outputs=result1.get("agent_outputs", {}),  # Include previous responses
        conversation_history=[],
        project_context={"project_name": "Demo App", "technology": "Python/FastAPI"},
        uploaded_files=[],
        next_agent="",
        final_response="",
        requested_agents=[],
        called_agent=""
    )
    
    print(f"User: {state2['user_request']}")
    result2 = await workflow.workflow.ainvoke(state2)
    
    for agent, response in result2.get("agent_outputs", {}).items():
        if agent not in result1.get("agent_outputs", {}):  # Only show new responses
            print(f"\n{agent.replace('_', ' ').title()}: {response[:200]}...")
    
    # Demo Scenario 3: Team dismissal and continuation
    print("\n\n📌 Scenario 3: Agent Dismissal and Focused Conversation")
    print("-" * 40)
    
    state3 = SDLCState(
        user_request="Thanks Jessica and Dave, you can drop off now. Alex, let's continue working on the implementation details.",
        current_phase="collaboration",
        agent_outputs=result2.get("agent_outputs", {}),
        conversation_history=[],
        project_context={"project_name": "Demo App", "technology": "Python/FastAPI"},
        uploaded_files=[],
        next_agent="",
        final_response="",
        requested_agents=[],
        called_agent=""
    )
    
    print(f"User: {state3['user_request']}")
    result3 = await workflow.workflow.ainvoke(state3)
    
    active_agents = len(result3.get("agent_outputs", {}))
    print(f"\nActive agents after dismissal: {active_agents}")
    
    for agent, response in result3.get("agent_outputs", {}).items():
        print(f"\n{agent.replace('_', ' ').title()}: {response[:200]}...")
    
    print("\n" + "=" * 60)
    print("✅ A2A Protocol Demo Complete!")
    print(f"📊 Total scenarios tested: 3")
    print(f"🎯 Key features demonstrated:")
    print("   • Direct agent addressing by name")
    print("   • Agent-to-agent collaboration triggers")
    print("   • Multi-agent coordination")
    print("   • Agent dismissal and conversation focus")
    print("   • Context preservation across interactions")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(demo_a2a_protocol())