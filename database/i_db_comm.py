
class IDbComm:

    def add_event_type(self, event_type_name):
        pass

    def add_force_type(self, force_type_name):
        pass

    def get_event_types(self):
        pass

    def get_force_types(self):
        pass

    def get_all_events(self):
        pass

    def get_all_forces(self):
        pass

    def get_all_open_events(self):
        pass

    def add_event(self, timestamp, name, latitude, longitude, type_id, num_participants, description):
        pass

    def add_force(self, name, latitude, longitude, type_id):
        pass

    def update_force_pos(self, force_id, latitude, longitude):
        pass

    def close_event(self, event_id):
        pass

    def connect_force_to_event(self, force_id, event_id):
        pass

    def free_force(self, force_id):
        pass


