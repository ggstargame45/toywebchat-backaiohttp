from aiohttp import web
import aiohttp_cors
import os
from app.presentation.routes import init_routes
from app.presentation.websocket import websocket_handler
from app.infrastructure.redis_repository import RedisRepository
from app.application.services import ChatService

#TODO : 외부에서 접속 가능하게 하기
def create_app():
    app = web.Application()
    app['websockets'] = set()

    redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379')
    redis_repo = RedisRepository(redis_url=redis_url)
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

if __name__ == '__main__':
    app = create_app()
    web.run_app(app, host='0.0.0.0', port=8080)
