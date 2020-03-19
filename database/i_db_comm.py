
class IDbComm:
    def add_force(self, name, lat, lon, force_type_name, event_id=-1):
        pass

    def add_event(self, name, lat, lon, event_type_name, num_participants):
        pass

    def add_event_type_id(self, event_type_id, event_type_name):
        pass

    def add_force_type_id(self, force_type_id, force_type_name):
        pass

    def get_all_events(self):
        pass


