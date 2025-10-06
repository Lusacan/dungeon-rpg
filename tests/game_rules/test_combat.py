import unittest
from dungeon_rpg.entities import entity
from dungeon_rpg.game_rules.combat import Combat
from io import StringIO
from unittest.mock import patch

class CombatTest(unittest.TestCase):
    def test_successful_attack(self):
        # Melee attack: 36 (18 + 18)
        attacker = entity.Entity(18, 18, 10, 10, 10, 10, 5, "A")
        # Melee defense: 70 (60 + 10)
        # Health: 18 Pain Tolerance: 36
        defender = entity.Entity(10, 10, 18, 10, 18, 10, 1, "D")

        Combat.melee_attack(attacker, defender, attack_roll=40, damage_roll=4)
        self.assertEqual(defender.health, 18)
        self.assertEqual(defender.pain_tolerance, 32)

    def test_failed_attack(self):
        attacker = entity.Entity(18, 18, 10, 10, 10, 10, 5, "A")
        defender = entity.Entity(10, 10, 18, 10, 18, 10, 1, "D")

        Combat.melee_attack(attacker, defender, attack_roll=10, damage_roll=4)
        self.assertEqual(defender.health, 18)
        self.assertEqual(defender.pain_tolerance, 36)

    def test_fumble_attack(self):
        attacker = entity.Entity(18, 18, 10, 10, 10, 10, 5, "A")
        defender = entity.Entity(10, 10, 18, 10, 18, 10, 1, "D")

        combat_log = Combat.melee_attack(attacker, defender, attack_roll=1, damage_roll=4)

        self.assertIn("Critical failure!", combat_log)
        self.assertIn("A fumbles the attack!", combat_log)
        self.assertEqual(defender.health, 18)
        self.assertEqual(defender.pain_tolerance, 36)

    def test_critical_attack(self):
        attacker = entity.Entity(18, 18, 10, 10, 10, 10, 5, "A")
        defender = entity.Entity(10, 10, 18, 10, 18, 10, 1, "D")
        defender.melee_defense = 100

        combat_log = Combat.melee_attack(attacker, defender, attack_roll=100, damage_roll=4)
        self.assertIn("Critical hit!", combat_log)
        self.assertEqual(defender.health, 15)
        self.assertEqual(defender.pain_tolerance, 26)

    def test_overwhelming_attack(self):
        attacker = entity.Entity(18, 18, 10, 10, 10, 10, 5, "A")
        defender = entity.Entity(10, 5, 18, 10, 18, 10, 1, "D")

        combat_log = Combat.melee_attack(attacker, defender, attack_roll=99, damage_roll=4)
        self.assertIn("Overwhelming strike! D loses 4 health and 8 pain tolerance.", combat_log)
        self.assertEqual(defender.health, 14)
        self.assertEqual(defender.pain_tolerance, 28)

    def test_critical_and_overwhelm(self):
        attacker = entity.Entity(18, 18, 10, 10, 10, 10, 5, "A")
        defender = entity.Entity(10, 10, 18, 10, 18, 10, 1, "D")

        combat_log = Combat.melee_attack(attacker, defender, attack_roll=100, damage_roll=4)
        self.assertIn("Critical hit!", combat_log)
        self.assertIn("Overwhelming strike! D loses 7 health and 14 pain tolerance.", combat_log)
        self.assertEqual(defender.health, 11)
        self.assertEqual(defender.pain_tolerance, 22)

    def test_low_pain_tolerance(self):
        attacker = entity.Entity(18, 18, 10, 10, 10, 10, 5, "A")
        defender = entity.Entity(10, 10, 18, 10, 18, 10, 1, "D")
        defender.pain_tolerance = 3

        combat_log = Combat.melee_attack(attacker, defender, attack_roll=50, damage_roll=6)
        self.assertIn("Hit! D loses 3 health and 3 pain tolerance.", combat_log)
        self.assertEqual(defender.health, 15)
        self.assertEqual(defender.pain_tolerance, 0)

    def test_attack_equals_defense(self):
        attacker = entity.Entity(18, 18, 10, 10, 10, 10, 5, "A")
        defender = entity.Entity(10, 10, 18, 10, 18, 10, 1, "D")
        defense = defender.melee_defense
        attack_roll = defense - attacker.melee_attack

        combat_log = Combat.melee_attack(attacker, defender, attack_roll=attack_roll, damage_roll=5)
        self.assertIn("Miss!", combat_log)
        self.assertEqual(defender.health, 18)
        self.assertEqual(defender.pain_tolerance, 36)

    def test_defender_no_pain_tolerance(self):
        attacker = entity.Entity(18, 18, 10, 10, 10, 10, 5, "A")
        defender = entity.Entity(10, 10, 18, 10, 18, 0, 1, "D")
        defender.pain_tolerance = 0

        combat_log = Combat.melee_attack(attacker, defender, attack_roll=70, damage_roll=5)
        self.assertIn("Hit! D loses 5 health.", combat_log)
        self.assertEqual(defender.health, 13)
        self.assertEqual(defender.pain_tolerance, 0)

    def test_collateral_damage(self):
        attacker = entity.Entity(18, 18, 10, 10, 10, 10, 5, "A")
        defender = entity.Entity(10, 10, 18, 10, 18, 10, 1, "D")

        combat_log = Combat.melee_attack(attacker, defender, attack_roll=60, damage_roll=10)
        self.assertIn("Collateral damage: 2", combat_log)
        self.assertEqual(defender.health, 16)

    def test_defender_death(self):
        attacker = entity.Entity(18, 18, 10, 10, 10, 10, 5, "A")
        defender = entity.Entity(10, 10, 18, 10, 18, 10, 1, "D")

        Combat.melee_attack(attacker, defender, attack_roll=95, damage_roll=20)
        self.assertEqual(defender.health, 0)
        self.assertFalse(defender.is_alive())

if __name__ == "__main__":
    unittest.main()

