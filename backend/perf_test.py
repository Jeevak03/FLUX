# WebSocket Performance Test
import asyncio
import websockets
import json
import time

async def performance_test():
    """Test WebSocket response times with different message types"""
    
    test_messages = [
        {
            "name": "Simple Requirements",
            "payload": {
                "request": "What are the basic requirements for a todo app?",
                "context": {"project": "TodoApp", "tech_stack": "React"},
                "requested_agents": ["requirements_analyst"],
                "history": []
            }
        },
        {
            "name": "Multi-Agent Architecture",
            "payload": {
                "request": "Design the architecture for a real-time chat application",
                "context": {"project": "ChatApp", "tech_stack": "Node.js, WebSocket"},
                "requested_agents": ["requirements_analyst", "software_architect"],
                "history": []
            }
        }
    ]
    
    results = []
    
    for test in test_messages:
        print(f"\\n🧪 Testing: {test['name']}")
        
        try:
            start_time = time.time()
            
            async with websockets.connect('ws://localhost:8000/ws/perf_test_session') as websocket:
                # Send test message
                await websocket.send(json.dumps(test['payload']))
                print(f"📤 Sent request at {time.time() - start_time:.2f}s")
                
                first_response_time = None
                response_count = 0
                
                # Collect responses
                while True:
                    try:
                        response = await asyncio.wait_for(websocket.recv(), timeout=30.0)
                        data = json.loads(response)
                        
                        if first_response_time is None:
                            first_response_time = time.time() - start_time
                            print(f"⚡ First response at {first_response_time:.2f}s")
                        
                        if data.get('type') == 'agent_response':
                            response_count += 1
                            agent = data.get('agent', 'unknown')
                            elapsed = time.time() - start_time
                            print(f"🤖 {agent} responded at {elapsed:.2f}s")
                        
                        elif data.get('type') == 'status_update':
                            status = data.get('status')
                            if status == 'completed':
                                total_time = time.time() - start_time
                                print(f"✅ Completed in {total_time:.2f}s with {response_count} responses")
                                
                                results.append({
                                    'test': test['name'],
                                    'first_response': first_response_time,
                                    'total_time': total_time,
                                    'response_count': response_count
                                })
                                break
                            else:
                                elapsed = time.time() - start_time
                                details = data.get('details', status)
                                print(f"📊 Status at {elapsed:.2f}s: {details}")
                        
                    except asyncio.TimeoutError:
                        print("⏰ Test timed out")
                        break
        
        except Exception as e:
            print(f"❌ Test failed: {e}")
    
    # Summary
    print("\\n" + "="*60)
    print("🏆 PERFORMANCE TEST RESULTS")
    print("="*60)
    for result in results:
        print(f"Test: {result['test']}")
        print(f"  First Response: {result['first_response']:.2f}s")
        print(f"  Total Time: {result['total_time']:.2f}s") 
        print(f"  Responses: {result['response_count']}")
        print()

if __name__ == "__main__":
    asyncio.run(performance_test())