class ForceType:
    def __init__(self, force_type_id, force_type_name):
        self.force_type_id = force_type_id
        self.force_type_name = force_type_name

    def __repr__(self):
        return '''Force type number {}:
        force type name: {}'''.format(self.force_type_id, self.force_type_name)
