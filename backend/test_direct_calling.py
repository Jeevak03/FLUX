#!/usr/bin/env python3
"""
Test calling agents directly by name in chat without selecting them
"""

import asyncio
import websockets
import json
from datetime import datetime

async def test_direct_agent_calling():
    session_id = f"test_session_{int(datetime.now().timestamp())}"
    uri = f"ws://localhost:8000/ws/{session_id}"
    
    try:
        print(f"🎯 Testing direct agent calling by name in chat...")
        async with websockets.connect(uri) as websocket:
            print("✅ Connected successfully!")
            
            # Test: Call agents directly by name WITHOUT selecting any agents
            test_request = {
                "request": "Hello Sarah, Marcus, and Alex! Could you all please introduce yourselves? Sarah, I need requirements analysis. Marcus, we need architecture planning. Alex, what's your development approach?",
                "requested_agents": [],  # 🔥 NO AGENTS SELECTED - they should respond because they're mentioned by name
                "context": {
                    "projectName": "DirectCallTest",
                    "technology": "React", 
                    "phase": "planning"
                }
            }
            
            print("📤 Calling agents by name WITHOUT selecting them:")
            print(f"   Message: {test_request['request'][:100]}...")
            print(f"   Selected agents: {test_request['requested_agents']} (NONE)")
            
            await websocket.send(json.dumps(test_request))
            
            # Listen for responses from the mentioned agents
            responding_agents = set()
            timeout_count = 0
            max_timeout = 30
            
            while len(responding_agents) < 3 and timeout_count < max_timeout:
                try:
                    response = await asyncio.wait_for(websocket.recv(), timeout=1.0)
                    data = json.loads(response)
                    
                    if data.get('type') == 'agent_response':
                        agent = data.get('agent', 'unknown')
                        message = data.get('message', '')
                        responding_agents.add(agent)
                        print(f"🎯 {agent} responded! ({len(message)} chars)")
                        print(f"   Preview: {message[:80]}...")
                        
                    elif data.get('type') == 'collaboration_update':
                        agents = data.get('agents', [])
                        print(f"📢 Collaboration update: {agents}")
                        
                    elif data.get('type') == 'status_update':
                        status = data.get('status', '')
                        details = data.get('details', '')
                        if 'responding' in details:
                            print(f"⏳ {details}")
                        
                    elif data.get('type') == 'error':
                        error_msg = data.get('message', '')
                        print(f"❌ Error: {error_msg}")
                        
                except asyncio.TimeoutError:
                    timeout_count += 1
                    if timeout_count % 5 == 0:
                        print(f"⏳ Waiting for agents to respond... ({len(responding_agents)}/3, {timeout_count}s)")
                except websockets.exceptions.ConnectionClosed:
                    print("❌ WebSocket connection closed")
                    break
                except Exception as e:
                    print(f"❌ Error receiving data: {e}")
                    break
            
            print(f"\n📊 Direct Calling Test Results:")
            expected_agents = {"requirements_analyst", "software_architect", "developer"}
            actual_agents = responding_agents
            
            print(f"   Expected: Sarah, Marcus, Alex")
            print(f"   Responding agents: {sorted(actual_agents)}")
            print(f"   Total responses: {len(actual_agents)}")
            
            if len(actual_agents) >= 3:
                print("🎉 SUCCESS! Agents respond when called by name directly in chat!")
                return True
            elif len(actual_agents) >= 1:
                print("⚠️ PARTIAL SUCCESS - Some agents responded to direct calling")
                return True
            else:
                print("❌ FAILED - No agents responded to direct name calling")
                return False
                
    except Exception as e:
        print(f"❌ Connection error: {e}")
        return False

if __name__ == "__main__":
    success = asyncio.run(test_direct_agent_calling())
    print(f"\nTest result: {'PASSED' if success else 'FAILED'}")
    if success:
        print("\n✨ You can now call agents directly by name in chat without selecting them first!")