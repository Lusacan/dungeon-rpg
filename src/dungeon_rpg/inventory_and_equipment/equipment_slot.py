from dataclasses import dataclass
from typing import Optional
import dungeon_rpg.inventory_and_equipment.constants as ieconsts
    
@dataclass
class Slot:
    name: ieconsts.EquipmentSlot
    item: Optional[object] = None
    occupied: bool = False

    def equip(self, item):
        if not self.occupied:
            self.item = item
            self.occupied = True
        else:
            self.item = item
    
    def unequip(self):
        self.item = None
        self.occupied = False
    
    def set_occupied(self):
        self.occupied = not self.occupied
