from dungeon_rpg.inventory_and_equipment.item import Item
import dungeon_rpg.inventory_and_equipment.constants as iconsts

class Quest(Item):
    def __init__( self,
            name: str,
            item_type: iconsts.ItemType,
            weight: float,
            volume: float,
            quest_name: str = "",
            description: str = "",
            ) -> None:
        super().__init__(
            name,
            item_type,
            weight,
            volume,
            description)
        
        self.quest_name = quest_name
    