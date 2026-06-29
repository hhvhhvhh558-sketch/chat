import asyncio
import websockets
import os
import json

# Храним всех подключённых клиентов
connected = set()

async def handler(websocket, path):
    # Регистрируем нового клиента
    connected.add(websocket)
    try:
        async for message in websocket:
            # Рассылаем сообщение всем, кроме отправителя
            data = json.loads(message)
            broadcast_msg = json.dumps({"nick": data["nick"], "text": data["text"]})
            websockets.broadcast(connected, broadcast_msg)  # всем (можно исключить отправителя)
    finally:
        connected.remove(websocket)

async def main():
    port = int(os.environ.get("PORT", 8080))
    print(f"Запуск WebSocket сервера на порту {port}")
    async with websockets.serve(handler, "0.0.0.0", port):
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())