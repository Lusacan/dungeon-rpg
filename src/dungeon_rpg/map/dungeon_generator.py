import random
import dungeon_rpg.map.constants as mconstants
from dungeon_rpg.map.dungeon_room import DungeonRoom

class DungeonGenerator:
    """
    This class is responsible for generating the dungeon with rooms and corridors
    across infinite levels. With each progressing level enemies are getting stronger.
    """
    def __init__(self):
        self.dungeon = self.generate_dungeon()

    def generate_dungeon(self):
        room_size = random.choice(list(mconstants.RoomSize))

        if room_size == mconstants.RoomSize.SMALL:
            size_range = (5, 8)
        elif room_size == mconstants.RoomSize.MEDIUM:
            size_range = (9, 12)
        else:
            size_range = (13, 16)

        height = random.randint(*size_range)
        width = random.randint(*size_range)
        
        room = DungeonRoom(height, width, room_size)
        return room