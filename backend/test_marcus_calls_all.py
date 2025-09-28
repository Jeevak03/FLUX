#!/usr/bin/env python3
"""
Test Marcus calling multiple agents scenario
"""

import asyncio
import websockets
import json
from datetime import datetime

async def test_marcus_calls_multiple_agents():
    session_id = f"test_session_{int(datetime.now().timestamp())}"
    uri = f"ws://localhost:8000/ws/{session_id}"
    
    try:
        print(f"Testing Marcus calls multiple agents scenario...")
        async with websockets.connect(uri) as websocket:
            print("✅ Connected successfully!")
            
            # First, ask Sarah to call Marcus (to get Marcus active)
            print("Step 1: Getting Sarah and Marcus active...")
            test_request = {
                "request": "Sarah, please introduce yourself and ask Marcus to join our conversation.",
                "requested_agents": ["requirements_analyst"],
                "context": {
                    "projectName": "TestProject",
                    "technology": "React", 
                    "phase": "planning"
                }
            }
            
            await websocket.send(json.dumps(test_request))
            
            # Wait for both Sarah and Marcus to respond
            agents_seen = set()
            timeout = 0
            while len(agents_seen) < 2 and timeout < 20:
                try:
                    response = await asyncio.wait_for(websocket.recv(), timeout=1.0)
                    data = json.loads(response)
                    
                    if data.get('type') == 'agent_response':
                        agent = data.get('agent', 'unknown')
                        agents_seen.add(agent)
                        print(f"  ✅ {agent} responded")
                        
                except asyncio.TimeoutError:
                    timeout += 1
            
            if len(agents_seen) < 2:
                print("❌ Failed to get both Sarah and Marcus active")
                return False
            
            # Step 2: Ask Marcus to call the remaining 5 agents
            print("\nStep 2: Asking Marcus to introduce all remaining team members...")
            test_request2 = {
                "request": "Marcus, now please ask Alex Kim, Jessica Wu, David Singh, Emily Johnson, and Robert Chen to introduce themselves and join our team discussion.",
                "requested_agents": ["software_architect"],
                "context": {
                    "projectName": "TestProject",
                    "technology": "React", 
                    "phase": "planning"
                }
            }
            
            await websocket.send(json.dumps(test_request2))
            
            # Listen for all agents to respond
            final_agents = set(agents_seen)  # Start with existing agents
            timeout = 0
            max_timeout = 60  # 60 seconds for all agents
            
            while len(final_agents) < 7 and timeout < max_timeout:
                try:
                    response = await asyncio.wait_for(websocket.recv(), timeout=1.0)
                    data = json.loads(response)
                    
                    if data.get('type') == 'agent_response':
                        agent = data.get('agent', 'unknown')
                        if agent not in final_agents:
                            final_agents.add(agent)
                            message = data.get('message', '')
                            print(f"  🎯 NEW: {agent} joined! ({len(message)} chars)")
                            
                    elif data.get('type') == 'collaboration_update':
                        collaboration_agents = data.get('agents', [])
                        print(f"  📢 Collaboration update: {collaboration_agents}")
                        
                    elif data.get('type') == 'status_update':
                        details = data.get('details', '')
                        if 'responding' in details:
                            print(f"  ⏳ {details}")
                        
                except asyncio.TimeoutError:
                    timeout += 1
                    if timeout % 10 == 0:
                        print(f"  ⏳ Waiting for agents... ({len(final_agents)}/7 active, {timeout}s elapsed)")
            
            print(f"\n📊 Final Results:")
            expected_agents = {"requirements_analyst", "software_architect", "developer", "qa_tester", "devops_engineer", "project_manager", "security_expert"}
            missing_agents = expected_agents - final_agents
            
            print(f"   Total agents active: {len(final_agents)}/7")
            print(f"   Active agents: {sorted(final_agents)}")
            
            if missing_agents:
                print(f"   Missing agents: {sorted(missing_agents)}")
            
            if len(final_agents) == 7:
                print("🎉 SUCCESS! All 7 agents are now active after A2A communication!")
                return True
            else:
                print(f"⚠️ Only {len(final_agents)}/7 agents responded")
                return False
                
    except Exception as e:
        print(f"❌ Connection error: {e}")
        return False

if __name__ == "__main__":
    success = asyncio.run(test_marcus_calls_multiple_agents())
    print(f"\nTest result: {'PASSED' if success else 'FAILED'}")