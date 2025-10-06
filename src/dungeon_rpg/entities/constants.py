from enum import Enum, auto

starting_attribute_points = 81

class Race(Enum):
    HUMAN = auto()
    GOBLIN = auto()
    ORC = auto()
    DWARF = auto()
    ELF = auto()

available_races = [Race.HUMAN, Race.DWARF, Race.ELF]

race_info = {
    Race.HUMAN: {
        "description": "Balanced base attributes.",
        "modifiers": {}
    },
    Race.DWARF: {
        "description": "+2 Strength, +2 Endurance, -2 Dexterity, -1 Willpower, -1 Charisma.",
        "modifiers": {
            "Strength": 2,
            "Endurance": 2,
            "Dexterity": -2,
            "Willpower": -1,
            "Charisma": -1
        }
    },
    Race.ELF: {
        "description": "-2 Strength, +2 Dexterity, -2 Endurance, +1 Intelligence, +1 Charisma.",
        "modifiers": {
            "Strength": -2,
            "Dexterity": 2,
            "Endurance": -2,
            "Intelligence": 1,
            "Charisma": 1
        }
    },
}

class EntityType(Enum):
    HUMANOID = auto()
    UNDEAD = auto()
    ANIMAL = auto()

class Alignment(Enum):
    # Cannot be attacked
    FRIENDLY = auto()
    # Will automaticcally attack player
    HOSTILE = auto()
    # Attacks only when attacked
    NEUTRAL = auto()