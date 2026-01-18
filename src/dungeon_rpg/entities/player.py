from dungeon_rpg.entities.entity import Entity
from dungeon_rpg.inventory_and_equipment.inventory import Inventory
from dungeon_rpg.inventory_and_equipment.equipment import Equipment
import dungeon_rpg.inventory_and_equipment.constants as ieconsts
from dungeon_rpg.inventory_and_equipment.weapon import Weapon
import logging

class Player(Entity):
    """
    This class describes the player character and the belonging logic
    """
    def __init__(self, strength, dexterity, endurance, intelligence,
                 willpower, charisma, damage, id, race, name) -> None:
        super().__init__(strength, dexterity, endurance,
                         intelligence, willpower, charisma,
                         damage, id)
        self.race = race
        self.name : str = name
        self.inventory = Inventory(self.strength)
        self.equipment = Equipment()

        self.melee_attack_from_skill : int = 0
        self.melee_attack_from_weapon : int = 0
        #self.melee_attack_from_effect : int = 0
        self.melee_defense_from_skill : int = 0
        self.melee_defense_from_weapon : int = 0
        #self.melee_defense_from_effect : int = 0
        self.damage_from_skill : int = 0
        self.damage_from_weapon : int = 0
        #self.damage_from_effect : int = 0
        self.initiative_from_weapon : int = 0
        self.initiative_from_skill : int = 0
        self.initiative_from_effect : int = 0
        #self.effects -> effect class: curse, blessing, dot etc

    @property
    def melee_attack(self):
        #Get action cost check agains remaining
        base = super().melee_attack
        bonus = self.melee_attack_from_weapon + self.melee_attack_from_skill  
        return base + bonus
    
    @property
    def melee_defense(self):
        base = super().melee_defense
        bonus = self.melee_defense_from_weapon + self.melee_attack_from_skill
        return base + bonus
    
    @property
    def damage(self):
        return (super().damage + self.damage_from_weapon + self.damage_from_skill)
        #TODO: two weapon attack and damage? if no weapon return unamred + etc

    def apply_stats(self, source):
        self._modify_stats_from_source(source, +1)
        
    def remove_stats(self, source):
        self._modify_stats_from_source(source, -1)

    def _modify_stats_from_source(self, source, sign):
        if not hasattr(source, "stat_bonuses"):
            return
        
        for attr, value in source.stat_bonuses().items():
            setattr(self, attr, getattr(self, attr) + sign * value)

    def equip(self, item):
        if not item:
            return
        
        try:
            previous_item = self.equipment.equip_item(item)
        except ValueError:
            return False
        
        self.apply_stats(item)

        self.inventory.remove_item(item)

        if previous_item:
            self.inventory.add_item(previous_item)

        return True

    def unequip(self, slot):
        item = self.equipment.unequip_item(slot)
        if item:
            self.remove_stats(item)
            self.inventory.add_item(item)
        
    def pickup_item(self, item):
        return self.inventory.add_item(item)

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
