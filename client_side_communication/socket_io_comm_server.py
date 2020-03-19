from aiohttp import web
import socketio

sio = socketio.AsyncServer()
app = web.Application()
sio.attach(app)


class SocketIoCommServer:
    def __init__(self):
        self._clients = []
        web.run_app(app)
        print('upupu')


    @sio.event
    def connect(sid, environ):
        print("connect ", sid)
        print(environ)

        # send all info: force locations, active events

    @sio.event
    def disconnect(self):
        print('disconnect ', self)

    @sio.on('close_event')
    async def close_event(self, event_id):
        pass

    @sio.on('new_event')
    async def new_event(self, event_id):
        pass

    @sio.event
    async def chat_message(sid, data):
        print("message ", data)
        await sio.emit('reply', room=sid)

    '''
    pushes:
    - New event to HAMAL. Who takes care.
    - Hotspots
    - In connect i send to HAMAL all data(forces, events ACTIVE)
    '''

