import logging
import random
from dungeon_rpg.entities.entity import Entity

logging.basicConfig(
    filename="game.log",          # file to write logs
    filemode="w",                 # "a" for append, "w" for overwrite
    level=logging.DEBUG,          # minimum log level
    format="%(asctime)s [%(levelname)s] %(message)s"
)

class MovementLogic:
    def __init__(self, entity, dungeon):
        self.entity = entity
        self.dungeon = dungeon

        self.DIRECTIONS = {
            (-1, 0): "UP",
            (1, 0): "DOWN",
            (0, -1): "LEFT",
            (0, 1): "RIGHT",
            (0, 0): "STALL"
        }

    def approach_cell(self, coord_y, coord_x):
        dy = coord_y - self.entity.position_y
        dx = coord_x - self.entity.position_x

        new_x = self.entity.position_x
        new_y = self.entity.position_y

        if abs(dx) > abs(dy):
            new_x += 1 if dx > 0 else -1
        else:
            new_y += 1 if dy > 0 else -1

        logging.debug(f"Entity: {self.entity.name} Y:{self.entity.position_y} X:{self.entity.position_x}")

        cell = self.dungeon.get_cell(new_y, new_x)
        if cell.entity:
            dy, dx = self.get_direction(new_y, new_x)
            direction = self.DIRECTIONS.get((dy, dx), "UNKNOWN") #If not moved there is no direction
            logging.debug(f"Direction result:{direction}")
            if direction in ("UP", "DOWN"):
                logging.debug(f"Entity: {self.entity.name} in UP/DOWN")
                occupied_count_left = self.next_available_in_direction(new_y, new_x, 0, 1)
                occupied_count_right = self.next_available_in_direction(new_y, new_x, 0, -1)

                new_y = self.entity.position_y
                        
                cell_left = self.dungeon.get_cell(new_y, new_x - 1)
                cell_right = self.dungeon.get_cell(new_y, new_x + 1)

                if cell_left and cell_right and cell_left.entity and cell_right.entity:
                    new_y, new_x = self.step_back(dy, dx)

                if occupied_count_left > occupied_count_right:
                    if cell_right.entity is None:
                        new_x += 1
                    else:
                        new_x -= 1
                elif occupied_count_left < occupied_count_right:
                    if cell_left.entity is None:
                        new_x -= 1
                    else:
                        new_x += 1
                else:
                    if random.choice([True, False]):
                        new_x += 1
                    else:
                        new_x -= 1        

            elif direction in ("LEFT", "RIGHT"):
                logging.debug(f"Entity: {self.entity.name} in LEFT/RIGHT")
                occupied_count_up = self.next_available_in_direction(new_y, new_x, -1, 0)
                occupied_count_down = self.next_available_in_direction(new_y, new_x, 1, 0)

                new_x = self.entity.position_x
                        
                cell_up = self.dungeon.get_cell(new_y - 1, new_x)
                cell_down = self.dungeon.get_cell(new_y + 1, new_x)

                if cell_up and cell_down and cell_up.entity and cell_down.entity:
                    new_y, new_x = self.step_back(dy, dx)

                if occupied_count_up > occupied_count_down:
                    if cell_down.entity is None:
                        new_y -= 1
                    else:
                        new_y += 1 
                elif occupied_count_up < occupied_count_down:
                    if cell_up.entity is None:
                        new_y += 1  
                    else:
                        new_y -= 1
                else:
                    if random.choice([True, False]):
                        new_y += 1
                    else:
                        new_y -= 1         
            else:
                logging.debug(f"Direction UNKNOWN")
              
        message = self.dungeon.move_entity(self.entity, new_y, new_x)

        if message is None:
            logging.debug(f"Entity moving to: {self.entity.name} Y:{new_y} X:{new_x}")
            self.entity.position_x = new_x
            self.entity.position_y = new_y

        #TODO: verbose log for enemy movement instead of return
        logging.debug(f"{message}")
        return message
    
    def next_available_in_direction(self, new_y, new_x, dy: int, dx: int):
        """
        Check how many consecutive occupied cells exist in a given direction.
    
        dy, dx : step increments per iteration
            (-1, 0) → up
            (1, 0)  → down
            (0, -1) → left
            (0, 1)  → right
        """
        logging.debug(f"Counting occupied cells")
        occupied_count = 0
        while True:
            new_y += dy
            new_x += dx
            cell = self.dungeon.get_cell(new_y, new_x)
            if cell and cell.entity:
                occupied_count += 1
            else:
                break
        return occupied_count
    
    def get_in_range_to_cell(self, new_y, new_x):
        pass
    
    def is_next_to_cell(self, player):
        return abs(self.entity.position_x - player.position_x) <= 1 and \
               abs(self.entity.position_y - player.position_y) <= 1
    
    def get_direction(self, new_y, new_x):
        dy = new_y - self.entity.position_y
        dx = new_x - self.entity.position_x
        return (dy, dx)
    
    def reverse_direction(self, dy, dx):
        return -dy, -dx
    
    def step_back(self, dy, dx):
        rdy, rdx = self.reverse_direction(dy, dx)
        stepback_y = self.entity.position_y + rdy
        stepback_x = self.entity.position_x + rdx

        cell = self.dungeon.get_cell(stepback_y, stepback_x)
        if cell and not cell.entity:
            logging.debug(f"{self.entity.name} steps back...")
            return stepback_y, stepback_x
        else:
            logging.debug("No space to step back, staying in place.")
            return self.entity.position_y, self.entity.position_x