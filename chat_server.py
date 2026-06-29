import asyncio
import json
import os
import websockets

connected = set()

async def handler(websocket, path):
    connected.add(websocket)
    try:
        async for message in websocket:
            data = json.loads(message)
            broadcast = json.dumps({"nick": data["nick"], "text": data["text"]})
            # Рассылаем всем подключённым
            if connected:
                await asyncio.wait([ws.send(broadcast) for ws in connected])
    finally:
        connected.remove(websocket)

async def main():
    port = int(os.environ.get("PORT", 8080))
    print(f"WebSocket сервер запущен на порту {port}")
    async with websockets.serve(handler, "0.0.0.0", port):
        await asyncio.Future()  # бесконечное ожидание

if __name__ == "__main__":
    asyncio.run(main())