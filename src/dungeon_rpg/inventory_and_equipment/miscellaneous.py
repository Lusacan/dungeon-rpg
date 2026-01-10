from dungeon_rpg.inventory_and_equipment.item import Item
import dungeon_rpg.inventory_and_equipment.constants as iconsts

class Miscellaneous(Item):
    def __init__( self,
        name: str,
        item_type: iconsts.ItemType,
        weight: float,
        volume: float,
        misc_type: iconsts.MiscType,
        description: str = "",
        stackable: bool = False,
        quantity: int = 1,
        ) -> None:
        super().__init__(
            name,
            item_type,
            weight,
            volume,
            description,
            stackable,
            quantity)
            
        self.misc_type = misc_type

    @property
    def subtype_name(self):
        return iconsts.miscellaneous_type_string.get(self.misc_type, "Unknown")