import dungeon_rpg.inventory_and_equipment.constants as iconsts

class Item:
    def __init__( self,
        name: str,
        item_type: iconsts.ItemType,
        weight: float,
        volume: float,
        description: str,
        stackable: bool = False,
        quantity: int = 1,
    ) -> None: 
        self.name = name
        self.item_type = item_type
        self.weight = weight
        self.volume = volume
        self.description = description
        self.stackable = stackable
        self.quantity = quantity

    @property
    def quantity(self) -> int:
        return self._quantity
    
    @quantity.setter
    def quantity(self, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError("quantity must be int")
        if value < 1:
            raise ValueError("quantity must be >= 1")
        if not self.stackable and value != 1:
            raise ValueError("non-stackable items must have quantity = 1")
        self._quantity = value
    
    @property
    def type_name(self):
        return iconsts.item_type_string.get(self.item_type, "Unknown")
    
    @property
    def display_name(self) -> str:
        if self.stackable:
            return f"{self.name} ({getattr(self, 'quantity', 1)})"
        return self.name
    
    def __repr__(self):
        return(
            f"Item(name={self.name!r}, "
            f"type={self.type_name}, "
            f"weight={self.weight}, "
            f"volume={self.volume}, "
            f"description={self.description!r}, "
            f"stackable={self.stackable}, "
            f"quantity={self.quantity})"
        )