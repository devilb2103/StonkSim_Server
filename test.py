from aiohttp import web
import socketio

sio = socketio.AsyncServer()
app = web.Application()
sio.attach(app)

async def index(request):
    return web.Response(text="Hello World", content_type='text/html')

app.router.add_get('/', index)

@sio.event
async def connect(sid, env):
    # prints user id when that user connects (prints on server console)
    print(f"user with user id {sid} has connected")

@sio.event
async def disconnect(sid):
    # prints user id when that user disconnects (prints on server console)
    print(f"user with user id {sid} has disconnected")

@sio.on('message') # For when client sends ANY message with event "message"
async def insTicker(sid, message):
    # emits message to ALL clients value "pong" with event name "reply"
    await sio.emit(event="reply", data="pong")

@sio.on('me')
async def remTicker(sid, message):
    # sends that specific client their user id with event name "reply" if they send any message with event "me"
    await sio.emit(event="reply", data=f"you are {sid}", room=str(sid))

if __name__ == '__main__':
    web.run_app(app)
    # launches the app when you simply run the python script (press f5 lol)