#!/usr/bin/env python3

import asyncio
import concurrent.futures
import sys
import os
import json

import requests
import websockets

MM_URL = 'http://127.0.0.1:8065/api/v4'
MM_WSURL = 'ws://127.0.0.1:8065/api/v4/websocket'
MM_LOGIN = 'bot@localhost.local'
MM_PASSWORD = '12345678'
CALLBACK_URL = 'https://api.myapp.com/messages'


def login():
    loginData = {'login_id': MM_LOGIN, 'password': MM_PASSWORD}
    loginRequest = requests.post(MM_URL + '/users/login', json=loginData)
    if 'Token' in loginRequest.headers:
        return loginRequest.headers['Token']
    else:
        raise Exception("Authentification failed")


async def createConnection():
    async with websockets.connect(MM_WSURL) as websocket:
        await authenticateWebsocket(websocket)
        await startLoop(websocket)


async def startLoop(websocket):
    while True:
        try:
            await asyncio.wait_for(waitForMessage(websocket), timeout=60)
        except asyncio.TimeoutError:
            await websocket.pong()
            continue


async def authenticateWebsocket(websocket):
    jsonData = json.dumps({
        "seq": 1,
        "action": "authentication_challenge",
        "data": {
            "token": token
        }
    }).encode('utf8')
    await websocket.send(jsonData)
    response = await websocket.recv()
    status = json.loads(response)
    if 'event' in status and status['event'] == 'hello':
        print("Auth OK")
        return True
    else:
        return False


async def waitForMessage(websocket):
    while True:
        event = await websocket.recv()
        await eventHandler(event)

async def eventHandler(event):
    data = json.loads(event)
    if 'event' in data and data['event'] == 'posted':
        loop.run_in_executor(executor, messageTranslate, event)


def messageTranslate(message):
    requests.post(CALLBACK_URL, json=message)

loop = asyncio.get_event_loop()
executor = concurrent.futures.ThreadPoolExecutor(max_workers=os.cpu_count())

token = login()

try:
    sys.exit(loop.run_until_complete(createConnection()))
except KeyboardInterrupt:
    print("Shutting down, press Ctrl+C to force exit.", flush=True)

    def shutdown_exception_handler(l, context):
        if "exception" not in context \
                or not isinstance(context["exception"], asyncio.CancelledError):
            l.default_exception_handler(context)
    loop.set_exception_handler(shutdown_exception_handler)

    tasks = asyncio.gather(*asyncio.Task.all_tasks(loop=loop),
                           loop=loop,
                           return_exceptions=True)
    tasks.add_done_callback(lambda t: loop.stop())
    tasks.cancel()

    while not tasks.done() and not loop.is_closed():
        loop.run_forever()
finally:
    loop.close()
