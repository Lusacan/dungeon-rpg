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
        self._weight = 0.0
        self._volume = 0.0
        self.description = description
        self.stackable = stackable
        self.quantity = quantity

        self.unit_weight = weight
        self.unit_volume = volume

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
    def unit_weight(self) -> float:
        return self._weight

    @property
    def weight(self) -> float:
        return self._weight * self.quantity
    
    @unit_weight.setter
    def unit_weight(self, value: float) -> None:
        if not isinstance(value, (int, float)):
            raise TypeError("weight must be a number")
        if value < 0:
            raise ValueError("weight must be >= 0")
        self._weight = float(value)
    
    @property
    def unit_volume(self) -> float:
        return self._volume

    @property
    def volume(self) -> float:
        return self._volume * self.quantity

    @unit_volume.setter
    def unit_volume(self, value: float) -> None:
        if not isinstance(value, (int, float)):
            raise TypeError("volume must be a number")
        if value < 0:
            raise ValueError("volume must be >= 0")
        self._volume = float(value)
    
    @property
    def type_name(self):
        return iconsts.item_type_string.get(self.item_type, "Unknown")
    
    @property
    def display_name(self) -> str:
        if self.stackable:
            return f"{self.name} ({getattr(self, 'quantity', 1)})"
        return self.name
    
    def __repr__(self):
        attrs = ", ".join(f"{k}={v!r}" for k, v in vars(self).items()
        if not k.startswith("_"))
        return f"{self.__class__.__name__}({attrs})"