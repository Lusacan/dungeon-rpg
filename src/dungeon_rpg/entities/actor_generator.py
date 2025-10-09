import random
import dungeon_rpg.map.constants as mconsts
from dungeon_rpg.entities.constants import EntityType
from dungeon_rpg.entities.actor import Actor

class ActorGenerator:
    def __init__(self, difficulty = "", player_rating = 0):
        self.difficulty = difficulty
        self.player_rating = player_rating

    def generate_actors(self, dungeon, actor_type, actor_alignment, name : str):
        actor_cnt_min, actor_cnt_max = self.actor_count_limits(dungeon)
        actor_count = random.randint(actor_cnt_min, actor_cnt_max)
        
        actors = []

        for enemy_id in range(actor_count):
            enemy = Actor(12, 14, 11, 9, 9, 8, # Attributes TODO: Separate into method
                          4, # Damage
                          enemy_id+1,
                          actor_type,
                          actor_alignment,
                          f"{name}_{enemy_id+1}")

            while True:
                pos_y = random.randint(0, dungeon.height - 1)
                pos_x = random.randint(0, dungeon.width - 1)

                cell = dungeon.get_cell(pos_y, pos_x)
                if not cell.isBlocking:
                    enemy.position_y = pos_y
                    enemy.position_x = pos_x
                    break
            
            dungeon.place_entity(enemy, enemy.position_y, enemy.position_x)
            actors.append(enemy)
        return actors

    def actor_count_limits(self, dungeon):
        if dungeon.size == mconsts.RoomSize.SMALL:
            return (1, 3)
        elif dungeon.size == mconsts.RoomSize.MEDIUM:
            return (2, 4)
        else:
            return (3, 6)