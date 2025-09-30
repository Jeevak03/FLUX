#!/usr/bin/env python3
"""
Quick test script to verify agent routing is working correctly
"""

import asyncio
import json
from workflows.sdlc_workflow import SDLCWorkflow, SDLCState

async def test_direct_agent_call():
    """Test that 'Hi Marc' only calls Marc, not Sara"""
    
    print("=" * 60)
    print("🧪 Testing Direct Agent Call Fix")
    print("=" * 60)
    
    workflow = SDLCWorkflow()
    
    print("\n📝 Test: User says 'Hi Marc'")
    print("-" * 40)
    
    state = SDLCState(
        user_request="Hi Marc",
        current_phase="initial",
        agent_outputs={},
        conversation_history=[],
        project_context={},
        uploaded_files=[],
        next_agent="",
        final_response="",
        requested_agents=[],
        called_agent=None
    )
    
    print(f"✅ Input: \"{state['user_request']}\"")
    print(f"✅ Expected: Only Marc (software_architect) responds")
    
    try:
        result = await workflow.workflow.ainvoke(state)
        
        responding_agents = list(result.get("agent_outputs", {}).keys())
        
        print(f"\n📊 Result:")
        print(f"   Agents that responded: {responding_agents}")
        print(f"   Number of responses: {len(responding_agents)}")
        
        if len(responding_agents) == 1 and "software_architect" in responding_agents:
            print(f"\n✅ TEST PASSED!")
            print(f"   Only Marc responded as expected")
            return True
        else:
            print(f"\n❌ TEST FAILED!")
            if "requirements_analyst" in responding_agents:
                print(f"   Sara responded when she shouldn't have")
            if len(responding_agents) > 1:
                print(f"   Multiple agents responded: {responding_agents}")
            if len(responding_agents) == 0:
                print(f"   No agents responded!")
            return False
            
    except Exception as e:
        print(f"\n❌ TEST ERROR: {e}")
        return False

async def test_multi_agent_collaboration():
    """Test that explicit agent requests work"""
    
    print("\n\n" + "=" * 60)
    print("🧪 Testing Multi-Agent Collaboration")
    print("=" * 60)
    
    workflow = SDLCWorkflow()
    
    print("\n📝 Test: User says 'Please call Marc in to this chat' (Sara already active)")
    print("-" * 40)
    
    state = SDLCState(
        user_request="Please call Marc in to this chat",
        current_phase="collaboration",
        agent_outputs={"requirements_analyst": "I'm Sara, happy to help!"},
        conversation_history=[],
        project_context={},
        uploaded_files=[],
        next_agent="",
        final_response="",
        requested_agents=["requirements_analyst"],
        called_agent=None
    )
    
    print(f"✅ Input: \"{state['user_request']}\"")
    print(f"✅ Expected: Both Sara and Marc respond")
    
    try:
        result = await workflow.workflow.ainvoke(state)
        
        responding_agents = list(result.get("agent_outputs", {}).keys())
        
        print(f"\n📊 Result:")
        print(f"   Agents that responded: {responding_agents}")
        print(f"   Number of responses: {len(responding_agents)}")
        
        has_marc = "software_architect" in responding_agents
        has_sara = "requirements_analyst" in responding_agents
        
        if has_marc and has_sara:
            print(f"\n✅ TEST PASSED!")
            print(f"   Both Sara and Marc are in the conversation")
            return True
        else:
            print(f"\n❌ TEST FAILED!")
            if not has_marc:
                print(f"   Marc didn't join the conversation")
            if not has_sara:
                print(f"   Sara was removed from the conversation")
            return False
            
    except Exception as e:
        print(f"\n❌ TEST ERROR: {e}")
        return False

async def main():
    """Run all tests"""
    
    test1_pass = await test_direct_agent_call()
    test2_pass = await test_multi_agent_collaboration()
    
    print("\n\n" + "=" * 60)
    print("📋 TEST SUMMARY")
    print("=" * 60)
    print(f"Test 1 (Direct Call): {'✅ PASS' if test1_pass else '❌ FAIL'}")
    print(f"Test 2 (Multi-Agent): {'✅ PASS' if test2_pass else '❌ FAIL'}")
    
    if test1_pass and test2_pass:
        print(f"\n🎉 ALL TESTS PASSED!")
        print(f"The agent routing fix is working correctly.")
    else:
        print(f"\n⚠️  SOME TESTS FAILED")
        print(f"Please check the logs above for details.")
    
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(main())
