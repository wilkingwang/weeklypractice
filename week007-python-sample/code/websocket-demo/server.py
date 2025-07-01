import asyncio
import websockets
from datetime import datetime

async def handle(websocket):
    data = await websocket.recv()
    reply = f"Data received as \"{data}\". time: {datetime.now()}"
    print(reply)
    await websocket.send(reply)
    print("Send reply")

async def main():
    async with websockets.serve(handle, "localhost", 9999):
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())