from threading import Thread
from aiohttp import web
import socketio
from dataEmmiter import emitStockData
from dataWriter import addTicker, addUser, removeTicker, removeUser
from thread import thread

sio = socketio.AsyncServer()
app = web.Application()
sio.attach(app)
with open("data.csv", 'w') as csvfile:
    pass

############################# Initializations UP ^ ^ ^

############################# Working code DOWN
async def index(request):
    return web.Response(text="Hello World", content_type='text/html')

app.router.add_get('/', index)

@sio.event
async def connect(sid, env):
    await addUser(sio, sid)

@sio.event
async def disconnect(sid):
    await removeUser(sio, sid)

@sio.on('addTicker') # For when client adds a ticker against their ID
def insTicker(sid, message):
    addTicker(sid, message)

@sio.on('remTicker') # For when client removed a ticker against their ID
def remTicker(sid, message):
    removeTicker(sid, message)

async def init_app(): # app start wrapper that also launches emitStockData as a subprocess
    sio.start_background_task(emitStockData, sio)
    Thread(target=thread).start()
    return app

# threadProc = subprocess.Popen(["Python", "thread.py"])

if __name__ == '__main__':
    web.run_app(init_app())
    