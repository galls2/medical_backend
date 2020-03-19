
from json import JSONEncoder
import random

from ai.hotspot_recognizer import HotSpotRecognizer
from client_side_communication.socket_io_comm_server import SocketIoCommServer
from database.sqllite_db_comm import SqlLiteDbComm
from encoders.json_encoder import JsonEncoder
from pojos.event import Event


def generate_cluster(n_samples, x_mean, x_sigma, y_mean, y_sigma):
    events = []
    for i in range(n_samples):
        event = Event(0, 0, 0, random.gauss(x_mean, x_sigma), random.gauss(y_mean, y_sigma), 0, 0, 0)
        events.append(event)

    return events


def get_events():
    events = []
    events += generate_cluster(20, 10, 5, 30, 5)
    events += generate_cluster(20, 30, 5, 90, 5)
    events += generate_cluster(20, 70, 5, 20, 5)
    #
    # SIGMA = 1
    # events += generate_cluster(20, 0, SIGMA, 0, SIGMA)
    # events += generate_cluster(20, 20, SIGMA, 20, SIGMA)
    # events += generate_cluster(20, 40, SIGMA, 40, SIGMA)
    # events += generate_cluster(20, 100, SIGMA, 100, SIGMA)
    # events += generate_cluster(20, 60, SIGMA, 60, SIGMA)
    # events += generate_cluster(20, 80, SIGMA, 80, SIGMA)

    return events
def test():
    gen_events = get_events()
    recognizer = HotSpotRecognizer()
    hotspots = recognizer.recognize_hotspots(gen_events)
    for hotspot in hotspots:
        print(JsonEncoder().encode(hotspot))


if __name__ == '__main__':
    db = SqlLiteDbComm()
    print('DB up')
    s = SocketIoCommServer()
    print('Server up')
    test()
