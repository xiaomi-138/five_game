from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse # 【新增】导入返回文件的功能
from typing import List

app = FastAPI()

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

# 【新增核心功能】当有人访问这个网址的主页时，直接返回 intex.html 网页！
@app.get("/")
async def get_webpage():
    return FileResponse("intex.html")

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(data)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast("【系统通知】一位玩家离开了大厅")