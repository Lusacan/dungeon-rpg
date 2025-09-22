class Entity:
    """
    Base of every class that represent enemies
    or the player.
    """
    def __init__(self, strength: int, dexterity: int, endurance: int, 
                 intelligence: int, willpower:int, charisma: int, 
                 damage: int, id: str):
        self.strength = strength
        self.dexterity = dexterity
        self.endurance = endurance
        self.intelligence = intelligence
        self.willpower = willpower
        self.charisma = charisma
        self.id = id

        self.max_health = self.endurance
        self.health = self.max_health

        self.max_pain_tolerance = self.endurance + self.willpower
        self.pain_tolerance = self.max_pain_tolerance

        self.initiative = self.dexterity + self.intelligence
        self.melee_attack = self.strength + self.dexterity
        self.melee_defense = 60 + self.dexterity
        self.ranged_attack = self.dexterity
        self.ranged_defense = 50

        self.damage = damage

    @property
    def health(self):
        return self._health

    @health.setter
    def health(self, value):
        self._health = max(0, min(value, self.max_health))

    @property
    def pain_tolerance(self):
        return self._pain_tolerance

    @pain_tolerance.setter
    def pain_tolerance(self, value):
        self._pain_tolerance = max(0, min(value, self.max_pain_tolerance))

    def take_damage(self, dmg_hp: int, dmg_pt: int):
        # Health damage
        self.health -= dmg_hp
        if self.health < 0:
            self.health = 0
        # Pain tolerance damage
        self.pain_tolerance -= dmg_pt
        if self.pain_tolerance < 0:
            self.pain_tolerance = 0

    def is_alive(self):
        return self.health > 0
    
    def __repr__(self):
        return (f"Entity(str={self.strength}, dex={self.dexterity}, end={self.endurance}, "
            f"int={self.intelligence}, wil={self.willpower}, cha={self.charisma}, "
            f"HP={self.health}/{self.max_health}, PT={self.pain_tolerance}/{self.max_pain_tolerance})")
    
    def __str__(self):
        return (f"HP: {self.health}/{self.max_health}, "
            f"PT: {self.pain_tolerance}/{self.max_pain_tolerance}, "
            f"Attack: {self.melee_attack}, Defense: {self.melee_defense}")