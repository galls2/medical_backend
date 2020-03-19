import socketio

class SocketIoCommServer:
    def __init__(self, port):
        self._sio = socketio.AsyncServer()
        self._app = socketio.ASGIApp(self._sio)
