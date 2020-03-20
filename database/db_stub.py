from database.i_db_comm import IDbComm
from pojos.event import Event
from pojos.force import Force


class RamDB(IDbComm):
    def __init__(self):
        self._event_table = []
        self._event_idx = 0
        self._force_table = []
        self._force_idx = 0
        self._event_type_id_mapping = {}
        self._force_type_id_mapping = {}

    def add_force(self, name, lat, lon, force_type_name, event_id=-1):
        self._force_table.append(Force(self._force_idx, name, lat, lon, force_type_name, self._event_type_id_mapping[event_id]))
        self._force_idx += 1

    def add_event(self, timestamp, name, latitude, longitude, type_id, num_participants, description):
        self._event_table.append(Event(self._event_idx, timestamp, name, False, latitude, longitude, \
                                       self._event_type_id_mapping[self._event_idx], num_participants, description))
        self._event_idx += 1

    def add_event_type_id(self, event_type_id, event_type_name):
        self._event_type_id_mapping[event_type_id] = event_type_name

    def add_force_type_id(self, force_type_id, force_type_name):
        self._force_type_id_mapping[force_type_id] = force_type_name

    def get_all_events(self):
        return self._event_table

    def add_event_type(self, event_type_name):
        self._event_type_id_mapping[len(self._event_type_id_mapping.keys())] = event_type_name

    def add_force_type(self, force_type_name):
        self._force_type_id_mapping[len(self._force_type_id_mapping.keys())] = force_type_name

    def get_event_types(self):
        return self._event_type_id_mapping.values()

    def get_force_types(self):
        return self._force_type_id_mapping.values()

    def get_all_forces(self):
        return

    def get_all_open_events(self):
        pass

    def update_force_pos(self, force_id, latitude, longitude):
        pass

    def close_event(self, event_id):
        pass

    def connect_force_to_event(self, force_id, event_id):
        pass

    def free_force(self, force_id):
        pass

    def get_forces_by_event_id(self, event_id):
        pass
