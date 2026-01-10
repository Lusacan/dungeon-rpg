from dungeon_rpg.inventory_and_equipment.item import Item
import dungeon_rpg.inventory_and_equipment.constants as iconsts

#TODO: Create struct that describe material properties like: hardness, alchemical components ... etc

class Material(Item):
    def __init__( self,
        name: str,
        item_type: iconsts.ItemType,
        weight: float,
        volume: float,
        material_type: iconsts.MaterialType,
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

        self.material_type = material_type

    @property
    def subtype_name(self):
        return iconsts.material_type_string.get(self.material_type, "Unknown")