from enum import Enum, auto

class InventoryAndEquipment:
    DEFAULT_INVENTORY_CAPACITY = 5
    DEFAULT_INVENTORY_LOAD = 20

class ItemType(Enum):
    WEAPON = auto()
    ARMOR = auto()
    CONSUMABLE = auto()
    MATERIAL = auto()
    QUEST = auto()
    MISC = auto()

item_type_string = {
    ItemType.WEAPON: "Weapon",
    ItemType.ARMOR: "Armor",
    ItemType.CONSUMABLE: "Consumable",
    ItemType.MATERIAL: "Material",
    ItemType.QUEST: "Quest",
    ItemType.MISC: "Miscelanous"
}

class WeaponType(Enum):
    SWORD = auto()
    AXE = auto()
    MACE = auto()
    SHIELD = auto()
    QUIVER = auto()

class ArmorType(Enum):
    HEAD = auto()
    SHOULDER = auto()
    TORSO = auto()
    BRACE = auto()
    FEET = auto()
    LEGS = auto()
    HANDS = auto()

class EquipmentSlot(Enum):
    HEAD = auto()
    SHOULDER = auto()
    TORSO = auto()
    BRACE = auto()
    FEET = auto()
    LEGS = auto()
    HANDS = auto()
    LEFT_HAND = auto()
    RIGHT_HAND = auto()
    QUIVER = auto()

class Handness(Enum):
    ONE_HANDED = auto()
    TWO_HANDED = auto()
