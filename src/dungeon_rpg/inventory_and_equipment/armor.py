from dungeon_rpg.inventory_and_equipment.item import Item
import dungeon_rpg.inventory_and_equipment.constants as iconsts

class Armor(Item):
    def __init__( self,
        name: str,
        item_type: iconsts.ItemType,
        weight: float,
        volume: float,
        damage_absorption_value: int,
        movement_reduction_factor: int,
        armor_type: iconsts.ArmorType,
        description: str = ""
        ) -> None:
        super().__init__(name, item_type, weight, volume, description)
        self.armor_type = armor_type
        self.dav = damage_absorption_value
        self.mrf = movement_reduction_factor

    @property
    def subtype_name(self):
        return iconsts.armor_type_string.get(self.armor_type, "Unknown")