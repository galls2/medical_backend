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
    open_events = db.get_all_open_events()
    open_events_jsons = '[' + ' , '.join([JsonEncoder().encode(oevent) for oevent in open_events]) + ']'
    print(open_events_jsons)
    # await sio.emit('update_hotspots', forces_jsons)


async def send_forces_to_client(db):
    forces = db.get_all_forces()
    forces_jsons =  '[' + ' , '.join([JsonEncoder().encode(force) for force in forces]) + ']'
    print(forces_jsons)
    #await sio.emit('update_hotspots', forces_jsons)

async def send_hotspots_to_client(db):
    all_events = db.get_all_events()
    recognizer = HotSpotRecognizer()
    hotspots = recognizer.recognize_hotspots(all_events)

    hotspot_jsons = '[' + ' , '.join([JsonEncoder().encode(hotspot) for hotspot in hotspots]) + ']'
    print(hotspot_jsons)
    #await sio.emit('update_hotspots', hotspot_jsons)


def move_forces():
    #raise NotImplementedError()
    pass

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
