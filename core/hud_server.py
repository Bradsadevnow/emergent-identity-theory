
# hud_server.py
# Simple WebSocket broadcast server for the Halcyon HUD.
# Usage:
#   pip install websockets
#   python hud_server.py
# Then open hud.html in a browser (or multiple browsers) and point it at ws://localhost:8765

import asyncio
import websockets
import json
from typing import Set

CLIENTS: Set[websockets.WebSocketServerProtocol] = set()

async def handler(ws):
    CLIENTS.add(ws)
    try:
        async for msg in ws:
            # echo back? we treat incoming messages as broadcast payloads
            await broadcast(msg)
    except Exception:
        pass
    finally:
        CLIENTS.discard(ws)

async def broadcast(message: str):
    dead = []
    for c in CLIENTS:
        try:
            await c.send(message)
        except Exception:
            dead.append(c)
    for d in dead:
        CLIENTS.discard(d)

async def main():
    async with websockets.serve(handler, "127.0.0.1", 8765, ping_interval=20, ping_timeout=20):
        print("[HUD] WebSocket server running at ws://127.0.0.1:8765")
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())
