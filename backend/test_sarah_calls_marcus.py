#!/usr/bin/env python3
"""
Test Sarah calling Marcus scenario to reproduce the error
"""

import asyncio
import websockets
import json
from datetime import datetime

async def test_sarah_calls_marcus():
    session_id = f"test_session_{int(datetime.now().timestamp())}"
    uri = f"ws://localhost:8000/ws/{session_id}"
    
    try:
        print(f"Testing Sara calls Marcus scenario...")
        async with websockets.connect(uri) as websocket:
            print("✅ Connected successfully!")
            
            # Send Sarah a request to call Marcus
            test_request = {
                "request": "Hello Sarah! Please introduce yourself and then ask Marcus to join our conversation and introduce himself too.",
                "requested_agents": ["requirements_analyst"],  # Start with just Sarah
                "context": {
                    "projectName": "TestProject",
                    "technology": "React", 
                    "phase": "planning"
                }
            }
            
            print(f"📤 Asking Sarah to call Marcus...")
            await websocket.send(json.dumps(test_request))
            
            # Listen for responses and errors
            response_count = 0
            timeout_count = 0
            max_timeout = 30
            agents_seen = set()
            
            while timeout_count < max_timeout:
                try:
                    response = await asyncio.wait_for(websocket.recv(), timeout=1.0)
                    data = json.loads(response)
                    
                    if data.get('type') == 'agent_response':
                        agent = data.get('agent', 'unknown')
                        message = data.get('message', '')
                        agents_seen.add(agent)
                        print(f"🎯 Response from {agent}: {len(message)} chars")
                        print(f"   Preview: {message[:100]}...")
                        
                        # Check if Sarah mentions Marcus
                        if agent == "requirements_analyst" and "marcus" in message.lower():
                            print("   🔍 Sarah mentioned Marcus - A2A should trigger!")
                        
                    elif data.get('type') == 'status_update':
                        status = data.get('status', '')
                        details = data.get('details', '')
                        print(f"📥 Status: {status} - {details}")
                        
                    elif data.get('type') == 'error':
                        print(f"❌ Error received: {data.get('message', '')}")
                        return False
                        
                except asyncio.TimeoutError:
                    timeout_count += 1
                    if timeout_count % 5 == 0:
                        print(f"⏳ Waiting... ({timeout_count}s, agents: {list(agents_seen)})")
                except websockets.exceptions.ConnectionClosed:
                    print("❌ WebSocket connection closed")
                    break
                except Exception as e:
                    print(f"❌ Error receiving data: {e}")
                    break
            
            print(f"\n📊 Results:")
            print(f"   Agents that responded: {sorted(agents_seen)}")
            
            if "software_architect" in agents_seen:
                print("✅ SUCCESS - Marcus (software_architect) responded! A2A communication working!")
                return True
            elif len(agents_seen) >= 1:
                print("⚠️ Only Sarah responded - A2A communication may not have triggered")
                return False
            else:
                print("❌ No responses received")
                return False
                
    except Exception as e:
        print(f"❌ Connection error: {e}")
        return False

if __name__ == "__main__":
    success = asyncio.run(test_sarah_calls_marcus())
    print(f"\nTest result: {'PASSED' if success else 'FAILED'}")