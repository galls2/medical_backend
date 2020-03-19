from database.i_db_comm import IDbComm


class RamDB(IDbComm):
    def __init__(self):
        self._event_table = []
        self._event_idx = 0
        self._force_table = []
        self._force_idx = 0

    def add_force(self, name, lat, lon, force_type_name, event_id=-1):
        self._force_table.append((self._force_idx, name, lat, lon, force_type_name, event_id))
        self._force_idx += 1

    def add_event(self, name, lat, lon, event_type_name, num_participants):
        self._force_table.append((self, self._event_idx, name, lat, lon, event_type_name, num_participants))
        self._event_idx += 1

    def add_event_type_id(self, event_type_id, event_type_name):
        pass

    def add_force_type_id(self, force_type_id, force_type_name):
        pass

    def get_all_events(self):
        pass