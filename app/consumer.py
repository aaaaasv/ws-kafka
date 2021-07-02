import ast

from app.schemas import Message
from app.main import consumer


async def consume_messages():
    from app.websockets import websocket_manager
    async for msg in consumer:
        try:
            msg_dict = ast.literal_eval(msg.value.decode('UTF-8'))
            message = Message(**msg_dict)
            await websocket_manager.broadcast(message.json())
        except:
            continue
