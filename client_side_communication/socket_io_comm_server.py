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
        # send all info: force locations, active events, hotspots

    @sio.event
    def disconnect(self):
        print('disconnect ', self)

    @sio.on('close_event')
    async def close_event(self, event_id):
        pass

    @sio.on('new_event')
    async def new_event(self, event_id):
        # add to db
        # send message to HAMAL
        pass

    @sio.on('get_hotspots')
    async def get_hotspots(self):
        # get ALL events from DB
        # send after calc to HAMAL
        pass


#        await sio.emit('reply', room=sid)

if __name__ == '__main__':
    s = SocketIoCommServer()
    while True:
        x = 0
        print('gal')
