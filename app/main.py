from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import asyncio

from app.schemas import Message

from aiokafka import AIOKafkaConsumer
from starlette.endpoints import WebSocketEndpoint

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
            var ws = new WebSocket("ws://127.0.0.1:8000/ws/quickstart-events");
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('pre')
                var content = document.createTextNode(JSON.parse(event.data))
                message.appendChild(content)
                messages.appendChild(message)
                console.log(JSON.parse(event.data))
            };
        </script>
    </body>
</html>
"""


@app.get("/")
async def get():
    return HTMLResponse(html)


@app.websocket_route("/ws/{topic}")
class ConsumerApp(WebSocketEndpoint):

    async def on_connect(self, websocket):
        await websocket.accept()

        self.consumer = AIOKafkaConsumer(
            websocket.path_params['topic'],
            bootstrap_servers='localhost:9092',
        )
        await self.consumer.start()

        self.consume_task = asyncio.create_task(
            self.consume_messages(websocket)
        )

    async def on_disconnect(self, websocket, close_code):
        await websocket.close()
        await self.consumer.stop()
        self.consume_task.cancel()

    async def consume_messages(self, websocket):
        while True:
            async for msg in self.consumer:
                message = Message(
                    topic=msg.topic,
                    partition=msg.partition,
                    offset=msg.offset,
                    value=msg.value,
                    timestamp=msg.timestamp,
                    timestamp_type=msg.timestamp_type)

                await websocket.send_json(message.json())
