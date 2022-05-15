import asyncio
from websockets import serve
from base64 import b64encode

async def receive(websocket):
    print('Connected')
    async for message in websocket:
        print('|||', b64encode(message).decode('utf-8'))

async def main():
    async with serve(receive, "0.0.0.0", 6969):
        await asyncio.Future()  # run forever

asyncio.run(main())