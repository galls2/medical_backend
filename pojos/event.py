
class Event:
    def __init__(self, event_id, timestamp, name, latitude, longitude, type_id, num_participants, event_description):
        self.event_id = event_id
        self.timestamp = timestamp
        self.name = name
        self.latitude = latitude
        self.longitude = longitude
        self.type_id = type_id
        self.num_participants = num_participants
        self.event_description = event_description

