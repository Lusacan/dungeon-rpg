import unittest
from dungeon_rpg.entities import entity

class EntityTest(unittest.TestCase):
    def test_entity_creation(self):
        ent = entity.Entity(10, 10, 10, 10, 10, 10, 4, "T", "test")

         # Base stats
        self.assertEqual(ent.strength, 10)
        self.assertEqual(ent.dexterity, 10)
        self.assertEqual(ent.endurance, 10)
        self.assertEqual(ent.intelligence, 10)
        self.assertEqual(ent.willpower, 10)
        self.assertEqual(ent.charisma, 10)
        self.assertEqual(ent.id, "T")
        self.assertEqual(ent.name, "test")

        # Derived stats
        self.assertEqual(ent.max_health, 10)
        self.assertEqual(ent.health, 10)
        self.assertEqual(ent.max_pain_tolerance, 20)
        self.assertEqual(ent.pain_tolerance, 20)
        self.assertEqual(ent.initiative, 20)
        self.assertEqual(ent.melee_attack, 20)
        self.assertEqual(ent.melee_defense, 70)
        self.assertEqual(ent.ranged_attack, 10)
        self.assertEqual(ent.ranged_defense, 50)

    def test_take_damage(self):
        ent = entity.Entity(5, 5, 5, 5, 5, 5, 2, "T")

        ent.take_damage(1, 5)
        self.assertEqual(ent.health, 4)
        self.assertEqual(ent.pain_tolerance, 5)
        self.assertTrue(ent.is_alive())

        ent.take_damage(10, 20)
        self.assertEqual(ent.health, 0)
        self.assertEqual(ent.pain_tolerance, 0)
        self.assertFalse(ent.is_alive())

if __name__ == "__main__":
    unittest.main()