import unittest
from dungeon_rpg.entities import entity

class EntityTest(unittest.TestCase):
    def test_entity_creation(self):
        entity = entity.Entity(10, 10, 10, 10, 10, 10, 4, "T")

         # Base stats
        self.assertEqual(entity.strength, 10)
        self.assertEqual(entity.dexterity, 10)
        self.assertEqual(entity.endurance, 10)
        self.assertEqual(entity.intelligence, 10)
        self.assertEqual(entity.willpower, 10)
        self.assertEqual(entity.charisma, 10)
        self.assertEqual(entity.id, "T")

        # Derived stats
        self.assertEqual(entity.max_health, 10)
        self.assertEqual(entity.health, 10)
        self.assertEqual(entity.max_pain_tolerance, 20)
        self.assertEqual(entity.pain_tolerance, 20)
        self.assertEqual(entity.initiative, 20)
        self.assertEqual(entity.melee_attack, 20)
        self.assertEqual(entity.melee_defense, 70)
        self.assertEqual(entity.ranged_attack, 10)
        self.assertEqual(entity.ranged_defense, 50)

    def test_take_damage(self):
        entity = entity.Entity(5, 5, 5, 5, 5, 5, 2, "T")

        entity.take_damage(1, 5)
        self.assertEqual(entity.health, 4)
        self.assertEqual(entity.pain_tolerance, 5)
        self.assertTrue(entity.is_alive())

        entity.take_damage(10, 20)
        self.assertEqual(entity.health, 0)
        self.assertEqual(entity.pain_tolerance, 0)
        self.assertFalse(entity.is_alive())

if __name__ == "__main__":
    unittest.main()