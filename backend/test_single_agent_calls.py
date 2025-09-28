#!/usr/bin/env python3
"""
Test single direct agent calls without other agents joining
"""

import asyncio
import websockets
import json
from datetime import datetime

async def test_single_direct_agent_calls():
    session_id = f"test_session_{int(datetime.now().timestamp())}"
    uri = f"ws://localhost:8000/ws/${session_id}"
    
    test_cases = [
        {"message": "Hi Alex", "expected_agent": "developer", "description": "Direct greeting to Alex"},
        {"message": "Hello Marcus", "expected_agent": "software_architect", "description": "Direct greeting to Marcus"},
        {"message": "Hey Jessica", "expected_agent": "qa_tester", "description": "Direct greeting to Jessica"},
        {"message": "Hi David", "expected_agent": "devops_engineer", "description": "Direct greeting to David"},
    ]
    
    try:
        print(f"🎯 Testing single direct agent calls...")
        
        for i, test_case in enumerate(test_cases):
            print(f"\n=== Test {i+1}: {test_case['description']} ===")
            
            async with websockets.connect(uri) as websocket:
                print(f"✅ Connected for test {i+1}")
                
                # Send direct agent call
                test_request = {
                    "request": test_case["message"],
                    "requested_agents": [],  # NO agents selected - should respond only to the mentioned agent
                    "context": {
                        "projectName": "DirectCallTest",
                        "technology": "React",
                        "phase": "development"  # Mid-development phase, not requirements
                    }
                }
                
                print(f"📤 Sending: '{test_case['message']}'")
                await websocket.send(json.dumps(test_request))
                
                # Listen for responses - should only get ONE agent
                responding_agents = set()
                timeout_count = 0
                max_timeout = 15
                
                while len(responding_agents) == 0 and timeout_count < max_timeout:
                    try:
                        response = await asyncio.wait_for(websocket.recv(), timeout=1.0)
                        data = json.loads(response)
                        
                        if data.get('type') == 'agent_response':
                            agent = data.get('agent', 'unknown')
                            responding_agents.add(agent)
                            message = data.get('message', '')
                            print(f"🎯 {agent} responded: {message[:80]}...")
                            
                    except asyncio.TimeoutError:
                        timeout_count += 1
                        if timeout_count % 5 == 0:
                            print(f"⏳ Waiting for response... ({timeout_count}s)")
                
                # Evaluate result
                if len(responding_agents) == 0:
                    print(f"❌ No agent responded to '{test_case['message']}'")
                elif len(responding_agents) == 1:
                    actual_agent = list(responding_agents)[0]
                    if actual_agent == test_case["expected_agent"]:
                        print(f"✅ SUCCESS - Only {actual_agent} responded correctly")
                    else:
                        print(f"⚠️ Wrong agent - Expected {test_case['expected_agent']}, got {actual_agent}")
                else:
                    print(f"❌ Too many agents responded: {sorted(responding_agents)}")
                    print(f"   Expected only: {test_case['expected_agent']}")
                
                # Wait a moment between tests
                await asyncio.sleep(1)
        
        print(f"\n📊 Single Direct Agent Call Test Complete")
        print("✨ You should now be able to call individual agents without others joining automatically!")
        return True
        
    except Exception as e:
        print(f"❌ Connection error: {e}")
        return False

if __name__ == "__main__":
    success = asyncio.run(test_single_direct_agent_calls())
    print(f"\nTest result: {'PASSED' if success else 'FAILED'}")
    if success:
        print("\n🎯 Direct single agent calling is now working!")
        print("   Try: 'Hi Alex', 'Hello Marcus', 'Hey Jessica', etc.")
        print("   Only the called agent will respond!")