from fastapi import WebSocket

# 儲存所有連線中的 client
connected_clients: list[WebSocket] = []

async def connect_client(ws: WebSocket):
    await ws.accept()
    connected_clients.append(ws)

async def disconnect_client(ws: WebSocket):
    if ws in connected_clients:
        connected_clients.remove(ws)

async def broadcast(message: dict):
    # 廣播訊息給所有連線
    for ws in connected_clients[:]:  # 複製一份避免迴圈錯誤
        try:
            await ws.send_json(message)
        except:
            await disconnect_client(ws)
