from aiohttp import web
import aiohttp_cors
from app.presentation.routes import init_routes
from app.presentation.websocket import websocket_handler
from app.infrastructure.redis_repository import RedisRepository
from app.application.services import ChatService
import requests

import ssl

def create_app():
    app = web.Application()
    app['websockets'] = set()

    redis_repo = RedisRepository(redis_url='redis://localhost:6379')
    chat_service = ChatService(repository=redis_repo)
    app['chat_service'] = chat_service

    init_routes(app)
    app.router.add_get('/ws', websocket_handler)

    # Setup CORS
    cors = aiohttp_cors.setup(app, defaults={
        "*": aiohttp_cors.ResourceOptions(
            allow_credentials=True,
            expose_headers="*",
            allow_headers="*",
        )
    })

    # Apply CORS to all routes
    for route in list(app.router.routes()):
        cors.add(route)

    return app
def get_public_ip():
    try:
        response = requests.get('https://api.ipify.org?format=json')
        ip = response.json()['ip']
        return ip
    except requests.RequestException as e:
        print(f"Error fetching public IP: {e}")
        return None

if __name__ == '__main__':
    app = create_app()
    ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    ssl_context.load_cert_chain(certfile='./certtest.pem', keyfile='./keytest.pem')

    public_ip = get_public_ip()
    if public_ip:
        print(f"Server is running at https://{public_ip}:8080")
    else:
        print("Could not determine public IP address")

    web.run_app(app, host='0.0.0.0', port=8080, ssl_context=ssl_context)
