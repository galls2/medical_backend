import time
import random
from threading import Thread

from aiohttp import web
import socketio
from scipy.spatial import distance

from ai.hotspot_recognizer import HotSpotRecognizer
from encoders.json_encoder import JsonEncoder

sio = socketio.AsyncServer()
app = web.Application()
sio.attach(app)


async def send_events_to_client(db):
    open_events = db.get_all_open_events()
    open_events_jsons = '[' + ' , '.join([JsonEncoder().encode(oevent) for oevent in open_events]) + ']'
    print(open_events_jsons)
    await sio.emit('update_events', open_events_jsons)


async def send_forces_to_client(db):
    forces = db.get_all_forces()
    forces_jsons = '[' + ' , '.join([JsonEncoder().encode(force) for force in forces]) + ']'
    print(forces_jsons)
    await sio.emit('update_forces', forces_jsons)


async def send_hotspots_to_client(db):
    all_events = db.get_all_events()
    recognizer = HotSpotRecognizer()
    hotspots = recognizer.recognize_hotspots(all_events)

    hotspot_jsons = '[' + ' , '.join([JsonEncoder().encode(hotspot) for hotspot in hotspots]) + ']'
    print(hotspot_jsons)
    await sio.emit('update_hotspots', hotspot_jsons)


def stretch_legs(db, max_dist=0.1):
    forces = db.get_all_forces()
    for force in forces:
        new_long = force.longitude + random.uniform(-max_dist, max_dist)
        new_lat = force.latitude + random.uniform(-max_dist, max_dist)
        db.update_force_pos(force.force_id, new_lat, new_long)


async def send_update_to_client(db):
    await send_events_to_client(db)
    await send_forces_to_client(db)
    await send_hotspots_to_client(db)


def adopt_orphan_events(db):
    open_events = db.get_all_open_events()
    forces = db.get_all_forces()
    orphan_events = [open_event for open_event in open_events if \
                     all([force for force in forces if force.event_name != open_event.name])]

    for orphan_event in orphan_events:
        longitude = orphan_event.longitude
        latitude = orphan_event.latitude

        available_forces_locations = [(force.longitude, force.latitude) for force in forces if not force.event_name]
        if len(available_forces_locations) == 0:
            break
        force_idx_to_send = min([(distance.euclidean(available_forces_locations[f_idx], (longitude, latitude)), f_idx) \
                                 for f_idx in range(len(available_forces_locations))])[1]

        opt_force_id = forces[force_idx_to_send].force_id
        db.connect_force_to_event(opt_force_id, orphan_event.event_id)


async def background_task(db):
    count = 0
    print(db)
    while True:
        print('backgroundushim {}'.format(count))
        await send_update_to_client(db)
        #   await sio.emit('update_events', room=sid)
        stretch_legs(db)
        adopt_orphan_events(db)
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

    @sio.event
    def disconnect(self):
        print('disconnect ', self)

    @sio.on('close_event')
    async def close_event(self, event_id):
        self._db.close_event(event_id)
        force_ids = self._db.get_forces_by_event_id(event_id)
        [self._db.free_force(force_id) for force_id in force_ids]

    @sio.on('new_event')
    async def new_event(self, timestamp, name, latitude, longitude, type_id, num_participants, description):
        self._db.add_event(timestamp, name, latitude, longitude, type_id, num_participants, description)
