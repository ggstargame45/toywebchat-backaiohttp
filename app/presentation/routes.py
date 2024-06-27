from aiohttp import web

async def init_chat(request : web.Request):
    print(f"Init chat from {request.remote}")
    messages = request.app['chat_service'].get_messages()
    return web.json_response([msg.to_dict() for msg in messages])

async def chat_refresh(request : web.Request):
    request.app['chat_service'].delete_all_messages()
    return web.Response(text="All chat messages deleted.")

def init_routes(app):
    app.router.add_get('/chat-init', init_chat)
    app.router.add_post('/chat-refresh', chat_refresh)