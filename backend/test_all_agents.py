#!/usr/bin/env python3
"""
Test multi-agent introduction request
"""

import asyncio
import websockets
import json
from datetime import datetime

async def test_all_agents_introduction():
    session_id = f"test_session_{int(datetime.now().timestamp())}"
    uri = f"ws://localhost:8000/ws/{session_id}"
    
    try:
        print(f"Connecting to {uri}...")
        async with websockets.connect(uri) as websocket:
            print("✅ Connected successfully!")
            
            # Send a request that selects ALL 7 agents (like in your screenshot)
            test_request = {
                "request": "Hello team! Please introduce yourselves - Sarah, Marcus, Alex, Jessica, David, Emily, and Robert. I want to hear from everyone.",
                "requested_agents": [
                    "requirements_analyst",
                    "software_architect", 
                    "developer",
                    "qa_tester",
                    "devops_engineer",
                    "project_manager",
                    "security_expert"
                ],
                "context": {
                    "projectName": "TeamIntroduction",
                    "technology": "", 
                    "phase": "planning"
                }
            }
            
            print(f"📤 Sending request for ALL 7 agents: {test_request['requested_agents']}")
            await websocket.send(json.dumps(test_request))
            
            # Listen for responses from all agents
            agent_responses = {}
            timeout_count = 0
            max_timeout = 90  # 90 seconds for all agents
            
            while len(agent_responses) < 7 and timeout_count < max_timeout:
                try:
                    response = await asyncio.wait_for(websocket.recv(), timeout=1.0)
                    data = json.loads(response)
                    
                    if data.get('type') == 'agent_response':
                        agent = data.get('agent', 'unknown')
                        if agent not in agent_responses:
                            agent_responses[agent] = data.get('message', '')
                            print(f"🎯 Response from {agent}: {len(data.get('message', ''))} chars")
                            
                    elif data.get('type') == 'status_update':
                        print(f"📥 Status: {data.get('details', '')}")
                        
                except asyncio.TimeoutError:
                    timeout_count += 1
                    if timeout_count % 10 == 0:  # Print every 10 seconds
                        print(f"⏳ Waiting for agents... ({len(agent_responses)}/7 responded, {timeout_count}s elapsed)")
                except websockets.exceptions.ConnectionClosed:
                    print("❌ WebSocket connection closed")
                    break
                except Exception as e:
                    print(f"❌ Error receiving data: {e}")
                    break
            
            print(f"\n📊 Final Results:")
            print(f"   Agents responded: {sorted(agent_responses.keys())}")
            print(f"   Total responses: {len(agent_responses)}")
            
            expected_agents = {"requirements_analyst", "software_architect", "developer", "qa_tester", "devops_engineer", "project_manager", "security_expert"}
            actual_agents = set(agent_responses.keys())
            missing_agents = expected_agents - actual_agents
            
            if len(agent_responses) == 7:
                print("🎉 SUCCESS! All 7 agents responded with introductions!")
                return True
            else:
                print(f"⚠️ Only {len(agent_responses)}/7 agents responded")
                if missing_agents:
                    print(f"   Missing agents: {sorted(missing_agents)}")
                return False
                
    except Exception as e:
        print(f"❌ Connection error: {e}")
        return False

if __name__ == "__main__":
    success = asyncio.run(test_all_agents_introduction())
    print(f"\nTest result: {'PASSED' if success else 'FAILED'}")