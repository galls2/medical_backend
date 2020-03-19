import eventlet
import socketio

sio = socketio.Server()
app = socketio.WSGIApp(sio)


class SocketIoCommServer:
    def __init__(self):
        eventlet.wsgi.server(eventlet.listen(('', 5000)), app)
        print('upupu')
        self._clients = []

    @sio.event
    def connect(self, env):
        print('connection established to server')
        print(env)
        # send all info: force locations, active events

    #
    # @sio.on('close_event')
    # def close_event(self, event_id):
    #     pass
    #
    # @sio.on('new_event')
    # def new_event(self, event_id):
    #     pass

    '''
    pushes:
    - New event to HAMAL. Who takes care.
    - Hotspots
    - In connect i send to HAMAL all data(forces, events ACTIVE)
    '''


if __name__ == '__main__':
    s = SocketIoCommServer()
    while True:
        x = 0
        print('gal')
