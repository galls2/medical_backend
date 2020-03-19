
class Event:
    def __init__(self, event_id, timestamp, name, latitude, longitude, type_id, num_participants, event_description,
                 event_open):
        self.event_id = event_id
        self.timestamp = timestamp
        self.name = name
        self.latitude = latitude
        self.longitude = longitude
        self.type_id = type_id
        self.num_participants = num_participants
        self.event_description = event_description
        self.event_open = True if event_open else False

    def __repr__(self):
        return '''Event nubmer {}:
        time stamp: {}
        name: {}
        location: ({},{})
        type_id: {}
        number of participants: {}
        description: {}
        is it opened?: {}'''.format(self.event_id, self.timestamp, self.name, self.latitude, self.longitude,
                                    self.type_id, self.num_participants, self.event_description, self.event_open)
