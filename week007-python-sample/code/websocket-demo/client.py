import asyncio
import websockets
import time

async def ws_client(url):
    for i in range(1, 40):
        async with websockets.connect(url) as websocket:
            await websocket.send("Hello, I'm Python.")
            rsp = await websocket.recv()

        print(rsp)
        time.sleep(1)

asyncio.run(ws_client("ws://localhost:9999"))