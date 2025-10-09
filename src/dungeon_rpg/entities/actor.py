from dungeon_rpg.entities.entity import Entity
import dungeon_rpg.entities.constants as econsts
from dungeon_rpg.game_rules.combat import Combat
from dungeon_rpg.entities.movement_logic import MovementLogic

class Actor(Entity):
    """
    This class describes the actor and the belonging logic
    """
    def __init__(self, strength, dexterity, endurance, intelligence,
                 willpower, charisma, damage, id, entity_type, alignment, name):
        super().__init__(strength, dexterity, endurance,
                         intelligence, willpower, charisma,
                         damage, id,name)
        self.entity_type = entity_type
        self.alignment = alignment

    def behavior(self, player, dungeon):
        movement_logic = MovementLogic(self, dungeon)
        if self.alignment == econsts.Alignment.HOSTILE:
            if movement_logic.is_next_to_cell(player):
                return self.melee_attack_target(player)
            else:
                movement_logic.approach_cell(player.position_y, player.position_x)

    def melee_attack_target(self, target):   
        combat_log = Combat.melee_attack(self, target)
        return combat_log