from dungeon_rpg.inventory_and_equipment.item import Item

class Weapon(Item):
    def __init__(self, name, item_type, weight, volume, attack, 
                 defense, damage, speed, weapon_type, handedness):
        super.__init__(name, item_type, weight, volume)
        self.attack = attack
        self.defense = defense
        self.damage = damage
        self.speed = speed
        self.weapon_type = weapon_type
        self.handedness = handedness