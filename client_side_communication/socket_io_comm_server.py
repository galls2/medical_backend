import time
from threading import Thread

from aiohttp import web
import socketio

from ai.hotspot_recognizer import HotSpotRecognizer
from encoders.json_encoder import JsonEncoder

sio = socketio.AsyncServer()
app = web.Application()
sio.attach(app)


async def send_events_to_client(db):
    pass


async def send_forces_to_client(db):
    pass


async def send_hotspots_to_client(db):
    all_events = db.get_all_events()
    recognizer = HotSpotRecognizer()
    hotspots = recognizer.recognize_hotspots(all_events)
    print(JsonEncoder.encode(hotspots[0]))
    hotspot_jsons = '[' + ' , '.join([JsonEncoder.encode(hotspot) for hotspot in hotspots]) + ']'
    await sio.emit('reply', hotspot_jsons)


def move_forces():
    raise NotImplementedError()


async def send_update_to_client(db):
    await send_events_to_client(db)
    await send_forces_to_client(db)
    await send_hotspots_to_client(db)


async def background_task(db):
    count = 0
    print(db)
    while True:
        print('backgroundushim {}'.format(count))
        await send_update_to_client(db)
        #   await sio.emit('update_events', room=sid)
        move_forces()
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
