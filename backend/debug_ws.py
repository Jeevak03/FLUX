import asyncio
import websockets
import json

async def debug_test():
    try:
        async with websockets.connect('ws://localhost:8000/ws/debug_session') as ws:
            message = {
                'request': 'What are the requirements for a todo app?',
                'context': {'project': 'TodoApp'},
                'requested_agents': ['requirements_analyst'],
                'history': []
            }
            await ws.send(json.dumps(message))
            print('✅ Sent message')
            
            # Wait for responses
            for i in range(10):  # Max 10 responses
                try:
                    response = await asyncio.wait_for(ws.recv(), timeout=5.0)
                    data = json.loads(response)
                    msg_type = data.get('type', 'unknown')
                    status = data.get('status', data.get('agent', 'no_status'))
                    details = data.get('details', data.get('message', ''))[:100]
                    print(f'{i+1}: {msg_type} - {status}: {details}')
                    if data.get('type') == 'status_update' and data.get('status') == 'completed':
                        break
                except asyncio.TimeoutError:
                    print('⏱️ Timeout waiting for response')
                    break
    except Exception as e:
        print(f'❌ Error: {e}')

if __name__ == "__main__":
    asyncio.run(debug_test())