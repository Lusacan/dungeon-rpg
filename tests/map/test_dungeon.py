import unittest
from dungeon_rpg.map import dungeon_room
from dungeon_rpg.entities import entity
import dungeon_rpg.map.constants as mconsts

class DungeonTest(unittest.TestCase):
    def setUp(self):
        self.dun = dungeon_room.DungeonRoom(3, 3, mconsts.RoomSize.SMALL)
        self.ent = entity.Entity(5, 5, 5, 5, 5, 5, 2, "T")

    def test_dungeon_size(self):
        self.assertEqual(3, len(self.dun.grid))
        self.assertEqual(3, len(self.dun.grid[0]))
        self.assertEqual(mconsts.RoomSize.SMALL, self.dun.size)

    def test_place_entity_in_cell(self):
        self.dun.place_entity(self.ent, 1, 1)
        cell = self.dun.get_cell(1, 1)
        self.assertEqual(cell.entity, self.ent)
        self.assertTrue(cell.isBlocking)
    
    def test_bounds(self):
        with self.assertRaises(ValueError):
            self.dun.place_entity(self.ent, 4, 1)
        with self.assertRaises(ValueError):
            self.dun.place_entity(self.ent, -2, 1)

    def test_occupied_cell(self):
        self.dun.place_entity(self.ent, 1, 1)
        another = entity.Entity(5, 5, 5, 5, 5, 5, 2, "X")
        with self.assertRaises(ValueError):
            self.dun.place_entity(another, 1, 1)

    def test_remove_entity_from_cell(self):
        self.dun.place_entity(self.ent, 0, 0)
        self.dun.remove_entity(self.ent, 0, 0)
        cell = self.dun.get_cell(0, 0)
        self.assertIsNone(cell.entity)
        self.assertFalse(cell.isBlocking)

    def test_remove_wrong_entity_does_nothing(self):
        self.dun.place_entity(self.ent, 1, 1)
        another = entity.Entity(1, 1, 1, 1, 1, 1, 1, "X")
        self.dun.remove_entity(another, 1, 1)
        self.assertEqual(self.dun.get_cell(1, 1).entity, self.ent)

    def test_move_entity_success(self):
        self.dun.place_entity(self.ent, 0, 0)
        result = self.dun.move_entity(self.ent, 1, 1)
        self.assertIsNone(result)
        self.assertIsNone(self.dun.get_cell(0, 0).entity)
        self.assertEqual(self.dun.get_cell(1, 1).entity, self.ent)

    def test_move_entity_into_wall(self):
        self.dun.place_entity(self.ent, 2, 2)
        result = self.dun.move_entity(self.ent, 3, 3)
        self.assertEqual(result, "You hit the wall")

    def test_move_entity_into_occupied_cell(self):
        self.dun.place_entity(self.ent, 0, 0)
        blocker = entity.Entity(1, 1, 1, 1, 1, 1, 1, "B")
        self.dun.place_entity(blocker, 1, 0)
        result = self.dun.move_entity(self.ent, 1, 0)
        self.assertEqual(result, "Field is already occupied")

    def test_move_nonexistent_entity(self):
        result = self.dun.move_entity(self.ent, 1, 1)
        self.assertEqual(result, "Entity not found")

    def test_find_entity(self):
        self.dun.place_entity(self.ent, 2, 2)
        pos = self.dun.find_entity(self.ent)
        self.assertEqual(pos, (2, 2))

    def test_find_nonexistent_entity(self):
        pos = self.dun.find_entity(self.ent)
        self.assertIsNone(pos)


if __name__ == "__main__":
    unittest.main()
