from fastapi import APIRouter
from fastapi.responses import HTMLResponse

from starlette.endpoints import WebSocketEndpoint
from app.websockets import websocket_manager

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
            var ws = new WebSocket("ws://127.0.0.1:8001/ws");
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

router = APIRouter()


@router.get("/")
async def get():
    return HTMLResponse(html)


@router.websocket_route("/ws")
class ConsumerApp(WebSocketEndpoint):

    async def on_connect(self, websocket):
        await websocket_manager.connect(websocket)

    async def on_disconnect(self, websocket, close_code):
        websocket_manager.disconnect(websocket)
