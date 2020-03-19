class Force:
    def __init__(self, force_id, name, latitude, longitude, type_id, event_id):
        self.force_id = event_id
        self.name = name
        self.latitude = latitude
        self.longitude = longitude
        self.type_id = type_id
        self.event_id = event_id

    def __repr__(self):
        return '''Force Number {}:
        name: {}
        location: ({},{})
        type id: {}
        event_id: {}'''.format(self.force_id, self.name, self.latitude, self.longitude, self.type_id, self.event_id)




