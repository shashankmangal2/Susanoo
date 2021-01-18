#!/usr/bin/python3
import asyncio
import websockets

# async function to connect to a specified uri
async def ConnectionTesting(uri):
    async with websockets.connect(uri) as ws:
        # sending a message to the socket connected to the uri
        await ws.send("This is a command")
        # receiving a message from the connected socket        
        await ws.recv()

        await ws.send("This is sencond Command")

        await ws.recv()

asyncio.get_event_loop().run_until_complete(
    ConnectionTesting('ws://127.0.0.1:9090/test'))