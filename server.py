import asyncio
from websockets import serve
from base64 import b64decode

data = None

async def read():
    global data
    while True:
        loop = asyncio.get_event_loop()
        message = await loop.run_in_executor(None, input)
        if message.startswith('|||'):
            data = b64decode(message.split(' ')[-1].encode('utf-8')).decode('utf-8')


async def receive(websocket):
    global data
    async for message in websocket:
        if message == 'get' and data:
            await websocket.send(data)

async def server():
    async with serve(receive, "0.0.0.0", 7000):
        await asyncio.Future()  # run forever

async def main():
    await asyncio.gather(
        server(),
        read()
    ) # here we have two coroutines running parallely

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())