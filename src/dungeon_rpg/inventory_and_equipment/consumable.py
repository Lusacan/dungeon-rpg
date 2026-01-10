from dungeon_rpg.inventory_and_equipment.item import Item
import dungeon_rpg.inventory_and_equipment.constants as iconsts

class Consumable(Item):
    def __init__( self,
            name: str,
            item_type: iconsts.ItemType,
            weight: float,
            volume: float,
            consumable_type: iconsts.ConsumableType,
            description: str = "",
            quantity: int = 1,
            stackbale: bool = True
            ) -> None:
        super().__init__(
            name,
            item_type,
            weight,
            volume,
            description,
            stackable = stackbale,
            quantity = quantity)
        
        self.consumable_type = consumable_type
        self.quantity = quantity

    @property
    def subtype_name(self):
        return iconsts.consumable_type_string.get(self.consumable_type, "Unknown")
    