import time
import random
from threading import Thread

from aiohttp import web
import socketio
from scipy.spatial import distance

from ai.hotspot_recognizer import HotSpotRecognizer
from database.sqllite_db_comm import SqlLiteDbComm
from encoders.json_encoder import JsonEncoder
from pojos.event import Event

sio = socketio.AsyncServer(cors_allowed_origins="*")
app = web.Application()
sio.attach(app)


async def send_events_to_client(db):
    open_events = db.get_all_open_events()
    forces = db.get_all_forces()

    events_with_handlers = []
    for oevent in open_events:
        oevent.handlingForces = [force.name for force in forces if force.event_name == oevent.name]
        events_with_handlers.append(oevent)
    open_events_jsons = '[' + ' , '.join([JsonEncoder().encode(oevent) for oevent in events_with_handlers]) + ']'
    #  print(open_events_jsons)
    await sio.emit('update_events', open_events_jsons)


async def send_forces_to_client(db):
    forces = db.get_all_forces()
    forces_jsons = '[' + ' , '.join([JsonEncoder().encode(force) for force in forces]) + ']'
    # print(forces_jsons)
    await sio.emit('update_forces', forces_jsons)


async def send_hotspots_to_client(db):
    all_events = db.get_all_events()
    recognizer = HotSpotRecognizer()
    hotspots = recognizer.recognize_hotspots(all_events)

    hotspot_jsons = '[' + ' , '.join([JsonEncoder().encode(hotspot) for hotspot in hotspots]) + ']'
    # print(hotspot_jsons)
    await sio.emit('update_hotspots', hotspot_jsons)


def stretch_legs(db, max_dist=0.01):
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
                     all([force.event_name != open_event.name for force in forces])]

    for orphan_event in orphan_events:

        longitude = orphan_event.longitude
        latitude = orphan_event.latitude

        available_forces = [force for force in forces if not force.event_name]
        available_forces_locations = [(force.longitude, force.latitude) for force in available_forces]
        if len(available_forces_locations) == 0:
            break

        force_idx_to_send = min([(distance.euclidean(available_forces_locations[f_idx], (longitude, latitude)), f_idx) \
                                 for f_idx in range(len(available_forces_locations))])[1]
        opt_force_id = available_forces[force_idx_to_send].force_id
        #    print('>>>>>>Connecting force {} to event {}'.format(opt_force_id, orphan_event.event_id))
        db.connect_force_to_event(opt_force_id, orphan_event.event_id)
        forces = db.get_all_forces()


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
    def disconnect(sid):
        print('disconnect ', sid)

    @sio.on('close_event')
    async def close_event(sid, event_id):
        print('LALALLALALA I LOVE IT WHEN YOU CALL ME SENIORITA', event_id)
        db = SqlLiteDbComm()
        db.close_event(event_id)
        forces = db.get_forces_by_event_id(event_id)
        [db.free_force(force.force_id) for force in forces]

    @sio.on('new_event')
    async def new_event(sid, timestamp, name, latitude, longitude, type_name, num_participants, description):
        db = SqlLiteDbComm()
        event_types = db.get_event_types()
        rel_types = [etype.event_type_id for etype in event_types if etype.event_type_name == type_name]
        db.add_event(timestamp, name, latitude, longitude, rel_types[0], num_participants, description)
