from typing import List
import dungeon_rpg.inventory_and_equipment.constants as ieconsts
from dungeon_rpg.inventory_and_equipment.item import Item

class Inventory:
    def __init__(self, entity_strength):
        self.max_capacity = ieconsts.InventoryAndEquipment.DEFAULT_INVENTORY_CAPACITY
        self.max_load = self.calc_max_load(entity_strength)
        self.items : List[Item] = []

    @property
    def current_size(self) -> float:
        return sum(
            item.volume * getattr(item, "quantity", 1)
            for item in self.items
        )

    @property
    def current_weight(self) -> float:
        return sum(
            item.weight * getattr(item, "quantity", 1)
            for item in self.items
        )
    
    def calc_max_load(self, strength):
        str_remainder = max(0, strength - 10)
        return ieconsts.InventoryAndEquipment.DEFAULT_INVENTORY_LOAD + str_remainder
    
    def modify_capacity_limit(self, amount):
        self.max_capacity += amount
    
    def modify_load_limit(self, amount):
        self.max_load += amount

    def can_add_item(self, item : Item):
        item_volume = item.volume
        item_weight = item.weight
        if item.stackable:
            item_volume *= item.quantity
            item_weight *= item.quantity
        if self.current_size + item.volume > self.max_capacity:
            return False
        if self.current_weight + item.weight > self.max_load:
            return False
        return True

    def add_item(self, item : Item):
        if not isinstance(item, Item):
            raise TypeError(f"Inventory can only hold Item objects, got {type(item).__name__}")
        
        if self.can_add_item(item):
            if item.stackable:
                for inv_item in self.items:
                # Merge if same type and same misc/subtype (customize as needed)
                    if type(inv_item) == type(item) and inv_item.name == item.name:
                        inv_item.quantity += getattr(item, "quantity", 1)
                        return True             
            self.items.append(item)
            return True
        return False
    
    def remove_item(self, item : Item):
        if item in self.items:
            self.items.remove(item)
    
    def __str__(self):
    # Current code returns a generator for first item only — that’s wrong
        return ", ".join(item.name for item in self.items)