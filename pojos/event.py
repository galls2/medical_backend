
class Event:
    def __init__(self, event_id, timestamp, name, latitude, longitude, type_id, num_participants, event_description):
        self._event_id = event_id
        self._timestamp = timestamp
        self._name = name
        self._latitude = latitude
        self._longitude = longitude
        self._type_id = type_id
        self._num_participants = num_participants
        self._event_description = event_description

