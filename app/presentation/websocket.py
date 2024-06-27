import json
import logging
from aiohttp import web

logging.basicConfig(level=logging.INFO)

async def websocket_handler(request: web.Request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    request.app['websockets'].add(ws)
    logging.info(f"WebSocket connection opened: {ws}")

    try:
        async for msg in ws:
            if msg.type == web.WSMsgType.TEXT:
                data = json.loads(msg.data)
                chat_message = request.app['chat_service'].save_message(data['username'], data['message'])
                message_data = chat_message.to_dict()

                # Broadcast message to all connected clients
                disconnected_clients = []
                for ws_client in request.app['websockets']:
                    try:
                        if not ws_client.closed:
                            await ws_client.send_json(message_data)
                        else:
                            disconnected_clients.append(ws_client)
                    except ConnectionResetError as e:
                        logging.error(f"Connection reset error: {e}")
                        disconnected_clients.append(ws_client)
                    except Exception as e:
                        logging.error(f"Error sending message to client: {e}")

                # Remove disconnected clients
                for client in disconnected_clients:
                    request.app['websockets'].remove(client)
    except Exception as e:
        logging.error(f"Error in WebSocket handler: {e}")
    finally:
        request.app['websockets'].remove(ws)
        logging.info(f"WebSocket connection closed: {ws}")

    return ws
