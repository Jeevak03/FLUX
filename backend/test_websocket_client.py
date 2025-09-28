#!/usr/bin/env python3
"""
Simple WebSocket client to test the agent response flow
"""

import asyncio
import websockets
import json
from datetime import datetime

async def test_websocket_client():
    session_id = f"test_session_{int(datetime.now().timestamp())}"
    uri = f"ws://localhost:8000/ws/{session_id}"
    
    try:
        print(f"Connecting to {uri}...")
        async with websockets.connect(uri) as websocket:
            print("✅ Connected successfully!")
            
            # Send a test request that should trigger A2A communication
            test_request = {
                "request": "I need help planning a new mobile app project. Let's discuss the requirements, architecture, and development approach.",
                "requested_agents": ["requirements_analyst"],  # Start with just Sarah
                "context": {
                    "projectName": "MobileApp",
                    "technology": "React Native", 
                    "phase": "planning"
                }
            }
            
            print(f"📤 Sending request: {test_request['request']}")
            await websocket.send(json.dumps(test_request))
            
            # Listen for responses
            response_count = 0
            timeout_count = 0
            max_timeout = 60  # Increase timeout for A2A communication
            agent_responses = {}
            
            while response_count < 3 and timeout_count < max_timeout:  # Expect multiple responses
                try:
                    # Wait for response with 1 second timeout
                    response = await asyncio.wait_for(websocket.recv(), timeout=1.0)
                    data = json.loads(response)
                    
                    print(f"📥 Received: {data.get('type', 'unknown')} - {data.get('agent', '')}")
                    
                    if data.get('type') == 'agent_response':
                        agent = data.get('agent', 'unknown')
                        if agent not in agent_responses:
                            agent_responses[agent] = data.get('message', '')
                            response_count += 1
                            print(f"🎯 Got agent response from {agent}: {len(data.get('message', ''))} chars")
                            
                            if response_count >= 2:  # Got A2A responses
                                print("✅ A2A Communication working!")
                                break
                        
                except asyncio.TimeoutError:
                    timeout_count += 1
                    print(f"⏳ Waiting... ({timeout_count}/{max_timeout})")
                except websockets.exceptions.ConnectionClosed:
                    print("❌ WebSocket connection closed")
                    break
                except Exception as e:
                    print(f"❌ Error receiving data: {e}")
                    break
            
            print(f"\n📊 Final Results:")
            print(f"   Agents responded: {list(agent_responses.keys())}")
            print(f"   Total responses: {len(agent_responses)}")
            
            if len(agent_responses) > 1:
                print("✅ A2A Communication successful - multiple agents participated!")
            elif len(agent_responses) == 1:
                print("⚠️  Only single agent responded - A2A communication may not be triggered")
            else:
                print("❌ No agent responses received")
                
    except Exception as e:
        print(f"❌ Connection error: {e}")

if __name__ == "__main__":
    asyncio.run(test_websocket_client())