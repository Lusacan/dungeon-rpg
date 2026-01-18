from dataclasses import dataclass
from typing import Optional
import dungeon_rpg.inventory_and_equipment.constants as ieconsts
from dungeon_rpg.inventory_and_equipment.item import Item
    
@dataclass
class Slot:
    slot: ieconsts.EquipmentSlot
    item: Optional[Item] = None
    occupied: bool = False

    def equip(self, item):
        if not self.occupied:
            self.item = item
            self.occupied = True
        else:
            self.item = item
    
    def unequip(self):
        previous_item = self.item
        self.item = None
        self.occupied = False
        return previous_item
    
    def set_occupied(self):
        self.occupied = not self.occupied

    @property
    def slot_name(self):
        return ieconsts.equipment_slot_string.get(self.slot, "Unknown")
