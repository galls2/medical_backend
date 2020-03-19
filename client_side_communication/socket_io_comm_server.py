import time
from threading import Thread

from aiohttp import web
import socketio

from ai.hotspot_recognizer import HotSpotRecognizer
from encoders.json_encoder import JsonEncoder

sio = socketio.AsyncServer()
app = web.Application()
sio.attach(app)


async def background_task(db):
    count = 0
    print(db)
    while True:
        print('backgroundushim {}'.format(count))

     #   await sio.emit('update_events', room=sid)

        count += 1

        await sio.sleep(2)


class SocketIoCommServer:
    def __init__(self, db):
        self._clients = []
        self._db = db
        sio.start_background_task(background_task, db)
        web.run_app(app)

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

    def get_hotspots(self):
        all_events = self._db.get_all_events()
        recognizer = HotSpotRecognizer()
        hotspots = recognizer.recognize_hotspots(all_events)
        for hotspot in hotspots:
            print(JsonEncoder().encode(hotspot))
        return hotspots

#     await sio.emit('reply', room=sid)
# send after calc to HAMAL
