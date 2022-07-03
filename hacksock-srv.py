import asyncio
from time import sleep
import websockets
import ssl
import pathlib
import argparse

async def connection_thread(websocket):
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

async def websocket_serve(ssl=False, ssl_context=None):
    if ssl:
        print("Running hacksock server in SSL mode...")
        async with websockets.serve(connection_thread, args["host"], args["port"], ssl=ssl_context):
            await asyncio.Future()  # run forever
    else:
        print("Running hacksock server in plain-text mode...")
        async with websockets.serve(connection_thread, args["host"], args["port"]):
            await asyncio.Future()  # run forever

async def main():
    if args["ssl"]:
        ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        path_cert = pathlib.Path(__file__).with_name("cert.pem")
        path_key = pathlib.Path(__file__).with_name("key.pem")
        ssl_context.load_cert_chain(path_cert, keyfile=path_key)
        task = asyncio.create_task(websocket_serve(ssl=True, ssl_context=ssl_context))
    else:
        task = asyncio.create_task(websocket_serve(ssl=False))
    await task

parser = argparse.ArgumentParser()
parser.add_argument("--host", help="Host", type=str, required=True)
parser.add_argument("--port", help="Port", type=int, required=True)
parser.add_argument('--ssl', action='store_true')
args = vars(parser.parse_args())
asyncio.run(main())
