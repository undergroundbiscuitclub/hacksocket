import asyncio
import websockets
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--host", help="Host", type=str, required=True)
parser.add_argument("--port", help="Port", type=int, required=True)
args = vars(parser.parse_args())

async def echo(websocket):
    print(f"New Connection from {websocket.remote_address[0]} using id: {websocket.id}")
    try:
        async for message in websocket:
            if message == "endingwebsocket":
                print(f"Connection closed {websocket.remote_address[0]} using id: {websocket.id}")
                await websocket.close()
                return
            print(message)
            cmd = input(f'{websocket.id}> ')
            await websocket.send(cmd)
    except Exception as e:
            print(e)


async def main():
    async with websockets.serve(echo, args["host"], args["port"]):
        await asyncio.Future()  # run forever
asyncio.run(main())