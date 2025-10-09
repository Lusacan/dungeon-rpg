class DungeonCell:
    def __init__(self, coord_y, coord_x):
        self.coordinate_y = coord_y
        self.coordinate_x = coord_x

        self.entity = None
        self.items = []
        self.objects = []

        self.isBlocking = False

    def set_entity(self, entity):
        self.entity = entity
        self.isBlocking = True

    def remove_entity(self):
        self.entity = None
        self.isBlocking = False