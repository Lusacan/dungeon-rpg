from enum import Enum, auto
class Interface:
    WIDTH = 90
    BOX_SEPARATOR_DISTANCE = 1
    INFO_BOX_HEIGHT = 5
    DUNGEON_MAX_WIDTH = 16
    DUNGEON_MAX_HEIGHT = 16
    DUNGEON_BOX_PADDING_HEIGHT = 2
    DUNGEON_BOX_PADDING_WIDTH = 2
    DUNGEON_BOX_WIDTH = DUNGEON_MAX_WIDTH + DUNGEON_BOX_PADDING_WIDTH
    DUNGEON_BOX_HEIGHT = DUNGEON_MAX_HEIGHT + DUNGEON_BOX_PADDING_HEIGHT
    DIALOG_BOX_WIDTH = (WIDTH // 2) - (DUNGEON_BOX_WIDTH // 2) - BOX_SEPARATOR_DISTANCE
    #DOUBLE PADDING TO MATCH DUNGEON BOX TOTAL HEIGHT
    DIALOG_BOX_HEIGHT = DUNGEON_BOX_HEIGHT + DUNGEON_BOX_PADDING_HEIGHT
    EQUIPMENT_BOX_HEIGHT = DUNGEON_BOX_HEIGHT + DUNGEON_BOX_PADDING_HEIGHT
    EQUIPMENT_BOX_WIDTH = WIDTH - (WIDTH // 3) - BOX_SEPARATOR_DISTANCE
    DESCRIPTION_BOX_WIDTH = WIDTH - (WIDTH // 3 * 2)
    LOG_BOX_HEIGHT = 7
    LOG_BOX_WIDTH = WIDTH
    HEIGHT = INFO_BOX_HEIGHT + DUNGEON_BOX_HEIGHT + LOG_BOX_HEIGHT

class Symbols:
    PLAYER = "@"

class Inventory:
    #Sum: 58
    default_colum_names = [
        ("Name", 25),
        ("Type", 15),
        ("Weight", 9),
        ("Volume", 9),
    ]

    weapon_column_names = [
        ("Name", 25),
        ("Type", 8),
        ("Grip", 5),
        ("Att", 5),
        ("Def", 5),
        ("Dmg", 5),
        ("Spd", 5)
    ]

    armor_column_names = [
        ("Name", 25),
        ("Slot", 10),
        ("DA", 5),
        ("MR", 18)
    ]

    material_column_names = [
        ("Name", 25),
        ("Type", 8),
        ("Quantity", 25)
    ]

    consumables_column_names = [
        ("Name", 25),
        ("Type", 8),
        ("Quantity", 25)
    ]

    quest_column_names = [
        ("Name", 25),
        ("Type", 8),
        ("Quest", 25)
    ]

    misc_column_names = [
        ("Name", 25),
        ("Type", 8),
        ("Quantity", 25)
    ]

    available_lines = 17

class InventoryView(Enum):
    DEFAULT = auto()
    WEAPONS = auto()
    ARMORS = auto()
    CONSUMABLES = auto()
    MATERIALS = auto()
    QUESTS = auto()
    MISCS = auto()