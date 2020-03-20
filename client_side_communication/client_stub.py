import time

import socketio

sio = socketio.Client()


@sio.event
def connect():
    print('connection established')


@sio.event
def update_events(data):
    print('events received with ', data)


@sio.event
def update_forces(data):
    print('forces received with ', data)


@sio.event
def update_hotspots(data):
    print('hotspots received with ', data)


@sio.event
def disconnect():
    print('disconnected from server')


if __name__ == '__main__':
    sio.connect('http://localhost:8080')
    time.sleep(2)
    print('byte')
    sio.disconnect()
