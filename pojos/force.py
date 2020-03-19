class Force:
    def __init__(self, force_id, name, latitude, longitude, type_name, event_name):
        self.force_id = force_id
        self.name = name
        self.latitude = latitude
        self.longitude = longitude
        self.type_name = type_name
        self.event_name = event_name

    def __repr__(self):
        return '''Force Number {}:
        name: {}
        location: ({},{})
        type id: {}
        event_id: {}'''.format(self.force_id, self.name, self.latitude, self.longitude, self.type_name, self.event_name)




