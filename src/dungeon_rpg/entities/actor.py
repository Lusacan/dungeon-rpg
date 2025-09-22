from dungeon_rpg.entities.entity import Entity

class Actor(Entity):
    """
    This class describes the actor and the belonging logic
    """
    def __init__(self, strength, dexterity, endurance, intelligence,
                 willpower, charisma, damage, id, entity_type, aligment, name):
        super().__init__(strength, dexterity, endurance,
                         intelligence, willpower, charisma,
                         damage, id)
        self.entity_type = entity_type
        self.friendly = aligment
        self.name = name

    def behavior():
        pass