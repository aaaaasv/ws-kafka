import asyncio
import ast
from typing import List

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from aiokafka import AIOKafkaConsumer
from starlette.websockets import WebSocket
from starlette.endpoints import WebSocketEndpoint

from app.schemas import Message
from app import settings

app = FastAPI()

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Consumer</title>
    </head>
    <body>
        <h1></h1>
        <code id='messages'>
        </code>
        <script>
            var ws = new WebSocket("ws://127.0.0.1:8001/ws/quickstart-events");
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('pre')
                var content = document.createTextNode(JSON.parse(event.data))
                message.appendChild(content)
                messages.appendChild(message)
            };
        </script>
    </body>
</html>
"""

consumer: AIOKafkaConsumer


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
            await connection.send_json(message)


manager = ConnectionManager()


async def consume_messages():
    async for msg in consumer:
        try:
            msg_dict = ast.literal_eval(msg.value.decode('UTF-8'))
            message = Message(**msg_dict)
            await manager.broadcast(message.json())
        except:
            continue


@app.on_event('startup')
async def startup_event():
    global consumer
    consumer = AIOKafkaConsumer(
        *settings.KAFKA_TOPICS,
        bootstrap_servers=f'{settings.KAFKA_HOST}:{settings.KAFKA_PORT}',
    )

    await consumer.start()
    global consume_task
    consume_task = asyncio.create_task(
        consume_messages()
    )


@app.on_event('shutdown')
async def shutdown_event():
    await consumer.stop()
    consume_task.cancel()


@app.get("/")
async def get():
    return HTMLResponse(html)


@app.websocket_route("/ws/{topic}")
class ConsumerApp(WebSocketEndpoint):

    async def on_connect(self, websocket):
        await manager.connect(websocket)

    async def on_disconnect(self, websocket, close_code):
        manager.disconnect(websocket)
