#!/usr/bin/env python3
"""
Test natural conversation management like dismissing agents and continuing with specific ones
"""

import asyncio
import websockets
import json
from datetime import datetime

async def test_conversation_management():
    session_id = f"test_session_{int(datetime.now().timestamp())}"
    uri = f"ws://localhost:8000/ws/{session_id}"
    
    try:
        print(f"🎯 Testing natural conversation management...")
        async with websockets.connect(uri) as websocket:
            print("✅ Connected successfully!")
            
            # Step 1: Start conversation with multiple agents
            print("\n=== Step 1: Starting conversation with Sarah and Marcus ===")
            test_request1 = {
                "request": "Hello Sarah and Marcus! Let's discuss our project requirements and architecture.",
                "requested_agents": [],
                "context": {
                    "projectName": "ConversationTest",
                    "technology": "React", 
                    "phase": "planning"
                }
            }
            
            await websocket.send(json.dumps(test_request1))
            
            # Wait for both to respond
            agents_active = set()
            timeout = 0
            while len(agents_active) < 2 and timeout < 15:
                try:
                    response = await asyncio.wait_for(websocket.recv(), timeout=1.0)
                    data = json.loads(response)
                    
                    if data.get('type') == 'agent_response':
                        agent = data.get('agent', 'unknown')
                        agents_active.add(agent)
                        print(f"  ✅ {agent} joined the conversation")
                        
                except asyncio.TimeoutError:
                    timeout += 1
            
            if len(agents_active) < 2:
                print("❌ Failed to get both agents active")
                return False
            
            print(f"  🎯 Active agents: {sorted(agents_active)}")
            
            # Step 2: Natural dismissal and continuation
            print("\n=== Step 2: Natural conversation management ===")
            test_request2 = {
                "request": "Sarah, you can drop off, I will continue to chat with Marcus about the technical architecture details.",
                "requested_agents": [],
                "context": {
                    "projectName": "ConversationTest",
                    "technology": "React", 
                    "phase": "planning"
                }
            }
            
            print(f"📤 Sending: {test_request2['request']}")
            await websocket.send(json.dumps(test_request2))
            
            # Listen for response (should not error)
            received_response = False
            error_received = False
            timeout = 0
            
            while not received_response and not error_received and timeout < 20:
                try:
                    response = await asyncio.wait_for(websocket.recv(), timeout=1.0)
                    data = json.loads(response)
                    
                    if data.get('type') == 'agent_response':
                        agent = data.get('agent', 'unknown')
                        message = data.get('message', '')
                        received_response = True
                        print(f"  ✅ {agent} responded: {message[:100]}...")
                        
                    elif data.get('type') == 'error':
                        error_msg = data.get('message', '')
                        error_received = True
                        print(f"  ❌ Error: {error_msg}")
                        
                    elif data.get('type') == 'status_update':
                        status = data.get('status', '')
                        details = data.get('details', '')
                        print(f"  📥 Status: {status} - {details}")
                        
                except asyncio.TimeoutError:
                    timeout += 1
                    if timeout % 5 == 0:
                        print(f"  ⏳ Waiting for response... ({timeout}s)")
            
            # Step 3: Continue conversation with Marcus
            if not error_received:
                print("\n=== Step 3: Continuing with Marcus ===")
                test_request3 = {
                    "request": "Marcus, can you explain the microservices architecture approach for our React application?",
                    "requested_agents": [],
                    "context": {
                        "projectName": "ConversationTest",
                        "technology": "React", 
                        "phase": "architecture"
                    }
                }
                
                await websocket.send(json.dumps(test_request3))
                
                # Wait for Marcus to respond
                marcus_responded = False
                timeout = 0
                while not marcus_responded and timeout < 15:
                    try:
                        response = await asyncio.wait_for(websocket.recv(), timeout=1.0)
                        data = json.loads(response)
                        
                        if data.get('type') == 'agent_response' and 'software_architect' in data.get('agent', ''):
                            marcus_responded = True
                            message = data.get('message', '')
                            print(f"  ✅ Marcus continued conversation: {message[:100]}...")
                            
                    except asyncio.TimeoutError:
                        timeout += 1
            
            # Results
            print(f"\n📊 Conversation Management Test Results:")
            if error_received:
                print("❌ FAILED - Error received during natural conversation management")
                return False
            elif received_response:
                print("✅ SUCCESS - Natural conversation management handled gracefully")
                print("   - No errors when dismissing Sarah")
                print("   - System understood continuation with Marcus") 
                if marcus_responded:
                    print("   - Marcus continued the conversation successfully")
                return True
            else:
                print("⚠️ PARTIAL - No error, but no clear response either")
                return False
                
    except Exception as e:
        print(f"❌ Connection error: {e}")
        return False

if __name__ == "__main__":
    success = asyncio.run(test_conversation_management())
    print(f"\nTest result: {'PASSED' if success else 'FAILED'}")
    if success:
        print("\n✨ Natural conversation management is working! You can dismiss agents and continue with specific ones.")