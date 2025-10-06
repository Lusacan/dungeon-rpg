from enum import Enum, auto

class RoomSize(Enum):
    # Cannot be attacked
    SMALL = auto()
    # Will automaticcally attack player
    MEDIUM = auto()
    # Attacks only when attacked
    BIG = auto()

NEIGHBOR_CELLS = (
    (-1, -1),  # top left
    (-1, 0),   # top
    (-1, 1),   # top right
    (0, -1),   # left
    (0, 1),    # right
    (1, -1),   # bottom left
    (1, 0),    # bottom
    (1, 1)     # bottom right
)