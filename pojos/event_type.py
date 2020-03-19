class EventType:
    def __init__(self, event_type_id, event_type_name):
        self.event_type_id = event_type_id
        self.event_type_name = event_type_name

    def __repr__(self):
        return '''Event type number {}:
        event type name: {}'''.format(self.event_type_id, self.event_type_name)
