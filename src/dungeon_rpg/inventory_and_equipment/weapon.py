from dungeon_rpg.inventory_and_equipment.item import Item
import dungeon_rpg.inventory_and_equipment.constants as iconsts

class Weapon(Item):
    def __init__( self,
            name: str,
            item_type: iconsts.ItemType,
            weight: float,
            volume: float,
            attack: int, 
            defense: int,
            damage: int,
            speed: int,
            weapon_type: iconsts.WeaponType,
            handedness: iconsts.Handness,
            description: str = ""
            ) -> None:
        super().__init__(
            name,
            item_type,
            weight,
            volume,
            description)
        
        self.attack = attack
        self.defense = defense
        self.damage = damage
        self.speed = speed
        self.weapon_type = weapon_type
        self.handedness = handedness

    @property
    def subtype_name(self):
        return iconsts.weapon_type_string.get(self.weapon_type, "Unknown")
    
    @property
    def handness_name(self):
        return iconsts.handness_string.get(self.handedness, "Unknown")