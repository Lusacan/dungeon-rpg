import unittest
from types import SimpleNamespace
from dungeon_rpg.inventory_and_equipment.equipment import Equipment
import dungeon_rpg.inventory_and_equipment.constants as ieconsts


class TestEquipment(unittest.TestCase):
    def setUp(self):
        self.equipment = Equipment()

        self.sword = SimpleNamespace(
            item_type=ieconsts.ItemType.WEAPON,
            weapon_type=ieconsts.WeaponType.SWORD,
            handness=ieconsts.Handness.ONE_HANDED,
            weight=5,
            name="Iron Sword"
        )

        self.greatsword = SimpleNamespace(
            item_type=ieconsts.ItemType.WEAPON,
            weapon_type=ieconsts.WeaponType.SWORD,
            handness=ieconsts.Handness.TWO_HANDED,
            weight=10,
            name="Greatsword"
        )

        self.shield = SimpleNamespace(
            item_type=ieconsts.ItemType.WEAPON,
            weapon_type=ieconsts.WeaponType.SHIELD,
            handness=ieconsts.Handness.ONE_HANDED,
            weight=6,
            name="Steel Shield"
        )

        self.quiver = SimpleNamespace(
            item_type=ieconsts.ItemType.WEAPON,
            weapon_type=ieconsts.WeaponType.QUIVER,
            handness=ieconsts.Handness.ONE_HANDED,
            weight=3,
            name="Arrow Quiver"
        )

        self.helmet = SimpleNamespace(
            item_type=ieconsts.ItemType.ARMOR,
            armor_type=ieconsts.ArmorType.HEAD,
            weight=2,
            name="Leather Helmet"
        )

    def test_equip_one_handed_weapon(self):
        prev = self.equipment.equip_item(self.sword)
        self.assertIsNone(prev)
        left = self.equipment.weapon_slots[ieconsts.EquipmentSlot.LEFT_HAND]
        self.assertEqual(left.item, self.sword)
        self.assertEqual(self.equipment.weight_sum, self.sword.weight)

    def test_equip_two_handed_weapon(self):
        self.equipment.equip_item(self.greatsword)
        left = self.equipment.weapon_slots[ieconsts.EquipmentSlot.LEFT_HAND]
        right = self.equipment.weapon_slots[ieconsts.EquipmentSlot.RIGHT_HAND]
        self.assertTrue(left.occupied)
        self.assertTrue(right.occupied)
        self.assertEqual(left.item, self.greatsword)
        self.assertEqual(self.equipment.weight_sum, self.greatsword.weight)

    def test_equip_shield(self):
        self.equipment.equip_item(self.shield)
        right = self.equipment.weapon_slots[ieconsts.EquipmentSlot.RIGHT_HAND]
        self.assertEqual(right.item, self.shield)
        self.assertEqual(self.equipment.weight_sum, self.shield.weight)

    def test_replace_weapon(self):
        self.equipment.equip_item(self.sword)
        prev = self.equipment.equip_item(self.greatsword)
        self.assertEqual(prev, self.sword)
        self.assertEqual(self.equipment.weight_sum, self.greatsword.weight)

    def test_equip_armor(self):
        prev = self.equipment.equip_item(self.helmet)
        slot = self.equipment.armour_slots[ieconsts.EquipmentSlot.HEAD]
        self.assertEqual(slot.item, self.helmet)
        self.assertEqual(self.equipment.weight_sum, self.helmet.weight)
        self.assertIsNone(prev)

    def test_unequip_item(self):
        self.equipment.equip_item(self.sword)
        slot = self.equipment.weapon_slots[ieconsts.EquipmentSlot.LEFT_HAND]
        item = self.equipment.unequip_item(slot)
        self.assertIsNone(slot.item)
        self.assertEqual(self.equipment.weight_sum, 0)
        self.assertEqual(item, self.sword)


if __name__ == "__main__":
    unittest.main()
