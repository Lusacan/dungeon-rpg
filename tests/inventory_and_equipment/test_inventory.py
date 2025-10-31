import unittest
from types import SimpleNamespace

from dungeon_rpg.inventory_and_equipment.inventory import Inventory
import dungeon_rpg.inventory_and_equipment.constants as ieconsts


class TestInventory(unittest.TestCase):

    def setUp(self):
        # Setup default constants for test
        ieconsts.InventoryAndEquipment.DEFAULT_INVENTORY_CAPACITY = 10
        ieconsts.InventoryAndEquipment.DEFAULT_INVENTORY_LOAD = 15

        # Create a base inventory with average strength
        self.inv = Inventory(entity_strength=10)

        # Create some mock items using SimpleNamespace instead of real Item class
        self.small_item = SimpleNamespace(name="Small Rock", size=1, weight=1)
        self.medium_item = SimpleNamespace(name="Medium Rock", size=5, weight=3)
        self.heavy_item = SimpleNamespace(name="Huge Rock", size=10, weight=20)

    def test_initial_capacity_and_load(self):
        self.assertEqual(self.inv.max_capacity, 10)
        self.assertEqual(self.inv.max_load, 15)

    def test_load_increases_with_strength(self):
        strong_inv = Inventory(entity_strength=14)
        self.assertGreater(strong_inv.max_load, self.inv.max_load)

    def test_add_item_within_limits(self):
        result = self.inv.add_item(self.small_item)
        self.assertTrue(result)
        self.assertIn(self.small_item, self.inv.items)

    def test_add_item_exceeds_capacity(self):
        self.inv.items = [SimpleNamespace(size=9, weight=1)]
        result = self.inv.add_item(self.medium_item)
        self.assertFalse(result)

    def test_add_item_exceeds_weight(self):
        result = self.inv.add_item(self.heavy_item)
        self.assertFalse(result)

    def test_remove_item(self):
        self.inv.add_item(self.small_item)
        self.inv.remove_item(self.small_item)
        self.assertNotIn(self.small_item, self.inv.items)

    def test_current_size_and_weight(self):
        self.inv.add_item(self.small_item)
        self.inv.add_item(self.medium_item)
        self.assertEqual(self.inv.current_size, 6)
        self.assertEqual(self.inv.current_weight, 4)

    def test_modify_capacity_and_load(self):
        self.inv.modify_capacity_limit(5)
        self.inv.modify_load_limit(10)
        self.assertEqual(self.inv.max_capacity, 15)
        self.assertEqual(self.inv.max_load, 25)

    def test_str_representation(self):
        self.inv.add_item(self.small_item)
        result = "".join(self.inv.__str__())
        self.assertIn("Small Rock", result)


if __name__ == "__main__":
    unittest.main()

