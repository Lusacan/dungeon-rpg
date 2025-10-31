import dungeon_rpg.inventory_and_equipment.constants as iconsts

class Item:
    def __init__(self, name, item_type, weight, volume, description):
        self.name = name
        self.item_type = item_type
        self.weight = weight
        self.volume = volume
        self.description = description

    @property
    def type_name(self):
        return iconsts.item_type_string.get(self.item_type, "Unknown")