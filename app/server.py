#!/usr/bin/env python

from bottle import static_file, route, run
# from threading import Thread
import os

import asyncio
import websockets
import json
import bot
import re

clients = set()
my_bot = bot.Bot()

#serving index.html file on "http://localhost:9000"
def httpHandler():
    while True:
        @route('/')
        def index():
            static_file('index.css', root='./app')
            static_file('client.js', root='./app')
            return static_file("index.html", root='./app')

        @route('/<filename>')
        def server_static(filename):
            return static_file(filename, root='./app')

        #run(host='localhost', port=9000)
        run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))


async def receive_send(websocket, path):
    # Please write your code here

    print("new client")
    global clients
    clients.add(websocket)
    print(websocket)
    try:
        while True:
            msg = await websocket.recv()
            await asyncio.wait([ws.send(json.dumps({'data': msg})) for ws in clients])
            bot_res = my_bot.recv_message(msg)
            if bot_res != msg:
                await asyncio.wait([ws.send(json.dumps({'data': bot_res})) for ws in clients])

    except websockets.exceptions.ConnectionClosed:
        pass

    finally:
        print("remove")
        clients.remove(websocket)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    start_server = websockets.serve(receive_send, '0.0.0.0', port=3000)
    server = loop.run_until_complete(start_server)
    print('Listen')

    t = Thread(target=httpHandler)
    t.daemon = True
    t.start()

    try:
        loop.run_forever()
    finally:
        server.close()
        start_server.close()
        loop.close()
