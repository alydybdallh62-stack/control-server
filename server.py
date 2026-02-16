import asyncio
import websockets
import json

connected = {}

async def handler(websocket):
    async for message in websocket:
        data = json.loads(message)
        
        if data['type'] == 'REGISTER':
            device_id = data['deviceId']
            connected[device_id] = websocket
            print(f"✅ {device_id} connected")
            
        elif data['type'] == 'COMMAND':
            target = data['targetId']
            if target in connected:
                await connected[target].send(json.dumps({
                    'type': 'COMMAND',
                    'command': data['command']
                }))

async def main():
    async with websockets.serve(handler, "0.0.0.0", 8080):
        print("🚀 Server running")
        await asyncio.Future()

asyncio.run(main())
