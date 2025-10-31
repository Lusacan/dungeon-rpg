from dungeon_rpg.inventory_and_equipment.item import Item

class Armor(Item):
    def __init__(self, name, item_type, weight, volume, damage_absorption_value, 
                 movement_reduction_factor, armor_type):
        super.__init__(name, item_type, weight, volume)
        self.dav = damage_absorption_value
        self.armor_type = armor_type
        self.mrf = movement_reduction_factor