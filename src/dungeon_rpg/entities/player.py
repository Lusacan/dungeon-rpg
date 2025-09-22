from dungeon_rpg.entities.entity import Entity

class Player(Entity):
    """
    This class describes the player character and the belonging logic
    """
    def __init__(self, strength, dexterity, endurance, intelligence,
                 willpower, charisma, damage, id, race, name):
        super().__init__(strength, dexterity, endurance,
                         intelligence, willpower, charisma,
                         damage, id)
        self.race = race
        self.name = name

    def __repr__(self):
        return (f"Player(str={self.strength}, dex={self.dexterity}, end={self.endurance}, "
            f"int={self.intelligence}, wil={self.willpower}, cha={self.charisma}, "
            f"HP={self.health}/{self.max_health}, PT={self.pain_tolerance}/{self.max_pain_tolerance}), "
            f"Race={self.race}, Name={self.name}")
    
    def __str__(self):
        return (f"HP: {self.health}/{self.max_health}, "
            f"PT: {self.pain_tolerance}/{self.max_pain_tolerance}, "
            f"Attack: {self.melee_attack}, Defense: {self.melee_defense}")
