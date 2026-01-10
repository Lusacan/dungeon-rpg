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
    ItemType.MISC: "Miscellaneous"
}

class WeaponType(Enum):
    SWORD = auto()
    DAGGER = auto()
    AXE = auto()
    MACE = auto()
    SHIELD = auto()
    QUIVER = auto()

weapon_type_string = {
    WeaponType.SWORD: "Sword",
    WeaponType.DAGGER: "Dagger",
    WeaponType.AXE: "Axe",
    WeaponType.MACE: "Mace",
    WeaponType.SHIELD: "Shield",
    WeaponType.QUIVER: "Quiver"
}

class ArmorType(Enum):
    HEAD = auto()
    SHOULDER = auto()
    CHEST = auto()
    WRIST = auto()
    FEET = auto()
    LEGS = auto()
    HANDS = auto()
    WAIST = auto()

armor_type_string = {
    ArmorType.HEAD: "Head",
    ArmorType.SHOULDER: "Shoulders",
    ArmorType.CHEST: "Chest",
    ArmorType.WRIST: "Wrist",
    ArmorType.FEET: "Feet",
    ArmorType.LEGS: "Legs",
    ArmorType.HANDS: "Hands",
    ArmorType.WAIST: "Waist"
}

class ConsumableType(Enum):
    FOOD = auto()
    DRINK = auto()
    POTION = auto()

consumable_type_string = {
    ConsumableType.FOOD: "Food",
    ConsumableType.DRINK: "Drink",
    ConsumableType.POTION: "Potion"
}

class MiscType(Enum):
    KEY = auto()
    JUNK = auto()
    BOOK = auto()
    SCROLL = auto()
    USEABLE = auto()

miscellaneous_type_string = {
    MiscType.KEY: "Key",
    MiscType.JUNK: "Junk",
    MiscType.BOOK: "Book",
    MiscType.SCROLL: "Scroll",
    MiscType.USEABLE: "Useable"
}

class MaterialType(Enum):
    PLANT = auto()
    METAL = auto()
    ANIMAL = auto()
    MAGICAL = auto()

material_type_string = {
    MaterialType.PLANT: "Plant",
    MaterialType.METAL: "Metal",
    MaterialType.ANIMAL: "Animal",
    MaterialType.MAGICAL: "Magical",
}

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

handness_string = {
    Handness.ONE_HANDED: "1H",
    Handness.TWO_HANDED: "2H",
}