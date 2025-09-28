import asyncio
import websockets
import json

async def test_websocket():
    try:
        uri = "ws://localhost:8000/ws/test-session"
        async with websockets.connect(uri) as websocket:
            print("WebSocket connected successfully")

            # Send a test message
            test_message = {
                "request": "Hello, test message",
                "context": {},
                "requested_agents": ["requirements_analyst"],
                "history": []
            }
            await websocket.send(json.dumps(test_message))
            print("Sent test message")

            # Wait for response
            response = await websocket.recv()
            print(f"Received: {response}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_websocket())