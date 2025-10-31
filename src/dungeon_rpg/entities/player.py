from dungeon_rpg.entities.entity import Entity
from dungeon_rpg.inventory_and_equipment.inventory import Inventory
from dungeon_rpg.inventory_and_equipment.equipment import Equipment
import dungeon_rpg.inventory_and_equipment.constants as ieconsts

class Player(Entity):
    """
    This class describes the player character and the belonging logic
    """
    def __init__(self, strength, dexterity, endurance, intelligence,
                 willpower, charisma, damage, id, race, name):
        super().__init__(strength, dexterity, endurance,
                         intelligence, willpower, charisma,
                         damage, id)
        self.race = race
        self.name = name
        self.inventory = Inventory(self.strength)
        self.equipment = Equipment()

    def equip(self, item):
        item_in_slot = self.equipment.equip_item(item)
        if item_in_slot:
            self.inventory.add_item(item_in_slot)

    def unequip(self, slot):
        #TODO Provide slot from interface selection
        item_in_slot = self.equipment.unequip_item(slot)
        if item_in_slot:
            self.inventory.add_item(item_in_slot)

    def pickup_item(self, item):
        self.inventory.add_item(item)

    def drop_item(self, item):
        self.inventory.remove_item(item)
        return item

    def __repr__(self):
        return (f"Player(str={self.strength}, dex={self.dexterity}, end={self.endurance}, "
            f"int={self.intelligence}, wil={self.willpower}, cha={self.charisma}, "
            f"HP={self.health}/{self.max_health}, PT={self.pain_tolerance}/{self.max_pain_tolerance}), "
            f"Race={self.race}, Name={self.name}")
    
    def __str__(self):
        return (f"HP: {self.health}/{self.max_health}, "
            f"PT: {self.pain_tolerance}/{self.max_pain_tolerance}, "
            f"Attack: {self.melee_attack}, Defense: {self.melee_defense}, "
            f"Position: Y:{self.position_y} X:{self.position_x}")
