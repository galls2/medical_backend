
class Event:
    def __init__(self, event_id, timestamp, name, event_open, latitude, longitude, type_name, num_participants, event_description):
        self.event_id = event_id
        self.timestamp = timestamp
        self.name = name
        self.event_open = event_open == 1
        self.latitude = latitude
        self.longitude = longitude
        self.type_name = type_name
        self.num_participants = num_participants
        self.event_description = event_description

    def __repr__(self):
        return '''Event number {}:
        time stamp: {}
        name: {}
        location: ({},{})
        type: {}
        number of participants: {}
        description: {}
        is it open: {}'''.format(self.event_id, self.timestamp, self.name, self.latitude, self.longitude,
                                 self.type_name, self.num_participants, self.event_description, self.event_open)


