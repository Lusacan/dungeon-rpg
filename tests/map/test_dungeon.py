import unittest
from dungeon_rpg.map import dungeon
from dungeon_rpg.entities import entity

class DungeonTest(unittest.TestCase):
    def test_dungeon_size(self):
        dun = dungeon.Dungeon(10, 8)

        self.assertEqual(8, len(dun.grid))
        self.assertEqual(10, len(dun.grid[0]))

    def test_entity_placement(self):
        dun = dungeon.Dungeon(3, 3)
        entity = entity.Entity(5, 5, 5, 5, 5, 5, 2, "T")
        dun.place_entity(entity, 2, 2)
        self.assertEqual(dun.grid[2][2], entity)

    def test_entity_find(self):
        dun = dungeon.Dungeon(3, 3)
        entity = entity.Entity(5, 5, 5, 5, 5, 5, 2, "T")
        dun.place_entity(entity, 1, 2)
        y, x = dun.find_entity(entity)
        self.assertEqual(y, 1)
        self.assertEqual(x, 2)

    def test_bounds(self):
        dun = dungeon.Dungeon(3, 3)
        entity = entity.Entity(5, 5, 5, 5, 5, 5, 2, "T")
        with self.assertRaises(ValueError):
            dun.place_entity(entity, 4, 1)
        with self.assertRaises(ValueError):
            dun.place_entity(entity, -2, 1)


if __name__ == "__main__":
    unittest.main()
