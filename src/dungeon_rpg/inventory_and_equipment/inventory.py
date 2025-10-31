import dungeon_rpg.inventory_and_equipment.constants as ieconsts

class Inventory:
    def __init__(self, entity_strength):
        self.max_capacity = ieconsts.InventoryAndEquipment.DEFAULT_INVENTORY_CAPACITY
        self.max_load = self.calc_max_load(entity_strength)
        self.items = []

    @property
    def current_size(self):
        return sum(item.volume for item in self.items)

    @property
    def current_weight(self):
        return sum(item.weight for item in self.items)
    
    def calc_max_load(self, strength):
        str_remainder = max(0, strength - 10)
        return ieconsts.InventoryAndEquipment.DEFAULT_INVENTORY_LOAD + str_remainder
    
    def modify_capacity_limit(self, amount):
        self.max_capacity += amount
    
    def modify_load_limit(self, amount):
        self.max_load += amount

    def can_add_item(self, item):
        if self.current_size + item.volume > self.max_capacity:
            return False
        if self.current_weight + item.weight > self.max_load:
            return False
        return True

    def add_item(self, item):
        if self.can_add_item(item):
            self.items.append(item)
            return True
        return False
    
    def remove_item(self, item):
        if item in self.items:
            self.items.remove(item)
    
    def __str__(self):
        for item in self.items:
            return (f"{item.name}" for item in self.items)