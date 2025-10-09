from dungeon_rpg.map.cell import DungeonCell
class DungeonRoom:
    """
    Basic 2D list to represent a dungeon room.
    """
    def __init__(self, width: int, height: int, size):
        self.width = width
        self.height = height
        self.size = size

        self.init_cells()


    def init_cells(self):
        self.grid = [
            [DungeonCell(coord_y, coord_x) for coord_x in range(self.width)]
            for coord_y in range(self.height)
            ]
        
        
    def get_cell(self, y, x):
        if not self.is_valid_cell(y, x):
            return None
        return self.grid[y][x]
    

    def place_entity(self, entity, y: int, x: int):
        cell = self.get_cell(y, x)
        if not cell:
            raise ValueError("Position out of bounds")
        if cell.isBlocking:
            raise ValueError("Cell already occupied")
        cell.set_entity(entity)


    def remove_entity(self, entity, y: int, x: int):
        cell = self.get_cell(y, x)
        if cell and entity == cell.entity:
            cell.remove_entity()


    def find_entity(self, entity):
        for row in self.grid:
            for cell in row:
                if entity == cell.entity:
                    return (cell.coordinate_y, cell.coordinate_x)
        return None


    def move_entity(self, entity, new_y: int, new_x: int):
        old_pos = self.find_entity(entity)
        if not old_pos:
            return "Entity not found"
        
        old_y, old_x = old_pos
        old_cell = self.get_cell(old_y, old_x)
        new_cell = self.get_cell(new_y, new_x)
        
        if not new_cell:
            return "You hit the wall"
        if new_cell.isBlocking:
            return "Field is already occupied"

        old_cell.remove_entity() 
        new_cell.set_entity(entity)
        return None


    def is_valid_cell(self, y: int, x: int):
        return 0 <= x < self.width and 0 <= y < self.height


    def __str__(self):
        rows = []
        for row in self.grid:
            rows.append(" ".join(cell.entity.id if cell and cell.entity else "." for cell in row))
        return "\n".join(rows)