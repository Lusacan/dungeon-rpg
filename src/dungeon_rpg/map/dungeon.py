class Dungeon:
    """
    Basic 2D list to represent a dungeon room.
    """
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        # Empty grid filled with None (no entity)
        self.grid = [[None for _ in range(width)] for _ in range(height)]

    def place_entity(self, entity, y: int, x: int):
        if not(0 <= x < self.width and 0 <= y < self.height):
            raise ValueError("Position out of bounds")
        if self.grid[y][x] is not None:
            raise ValueError("Cell already occupied")
        self.grid[y][x] = entity

    def find_entity(self, entity):
        for y in range(self.height):
            for x in range(self.width):
                if self.grid[y][x] is entity:
                    return (y, x)
        return None

    def move_entity(self, entity, new_y: int, new_x: int):
        pos = self.find_entity(entity)
        if pos is None:
            raise ValueError("Entity not found in dungeon")
        
        if not(0 <= new_x < self.width and 0 <= new_y < self.height):
            raise ValueError("New position is out of bounds")
        
        if self.grid[new_y][new_x] is not None:
            raise ValueError("Field is already occupied")

        old_y, old_x = pos
        self.grid[old_y][old_x] = None 
        self.grid[new_x][new_y] = entity

    def __str__(self):
        rows = []
        for row in self.grid:
            rows.append(" ".join(cell.id if cell else "." for cell in row))
        return "\n".join(rows)