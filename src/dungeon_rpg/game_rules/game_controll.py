import curses
from functools import partial
import dungeon_rpg.entities.constants as econsts 
import dungeon_rpg.settings.constants as sconsts
from dungeon_rpg.game_rules.combat import Combat
from dungeon_rpg.ui.game_interface import GameInterface
from dungeon_rpg.ui.game_interface import InterfaceSections
from dungeon_rpg.map.dungeon_generator import DungeonGenerator
import dungeon_rpg.map.constants as mconsts
from dungeon_rpg.entities.actor_generator import ActorGenerator
from dungeon_rpg.game_rules.action import Action
from dungeon_rpg.inventory_and_equipment.item import Item
from dungeon_rpg.inventory_and_equipment.weapon import Weapon
from dungeon_rpg.inventory_and_equipment.armor import Armor
from dungeon_rpg.inventory_and_equipment.material import Material
from dungeon_rpg.inventory_and_equipment.consumable import Consumable
from dungeon_rpg.inventory_and_equipment.miscellaneous import Miscellaneous
from dungeon_rpg.inventory_and_equipment.quest import Quest
import dungeon_rpg.inventory_and_equipment.constants as iconsts

class GameControll:
    def __init__(self, player):
        self.dungeon_generator = DungeonGenerator()
        self.actor_generator = ActorGenerator("EASY", 10)
        self.player = player
        self.log = []
        self.log_cursor = 0
        self.available_actions = []

    def start_game(self):
        def main(stdscr):
            curses.curs_set(0)
            stdscr.clear()
            stdscr.nodelay(False)
            stdscr.keypad(True)
            curses.set_escdelay(25)

            dungeon = self.dungeon_generator.generate_dungeon()

            dungeon.place_entity(self.player, self.player.position_y, self.player.position_x)

            enemies = self.actor_generator.generate_actors(dungeon,
                                             econsts.EntityType.HUMANOID,
                                             econsts.Alignment.HOSTILE,
                                             "Goblin")

            self.player.position_x = 0
            self.player.position_y = 0

            test_item_misc = Miscellaneous("Book of revelation",
                                       iconsts.ItemType.MISC,
                                       0.0,
                                       0.0,
                                       iconsts.MiscType.BOOK,
                                       "It contains the secrets of the universe")

            test_item_consumable = Consumable("Potion of health",
                                    iconsts.ItemType.CONSUMABLE,
                                    0.1,
                                    0.1,
                                    iconsts.ConsumableType.POTION,
                                    "Restores 5 healthpoints",
                                    quantity=3)

            test_item_quest_1 = Quest("First item",
                                      iconsts.ItemType.QUEST,
                                      0.0,
                                      0.0,
                                      "Development",
                                      "Marks the beginning of inventory")

            test_item_quest_2 = Quest("Last item",
                                      iconsts.ItemType.QUEST,
                                      0.0,
                                      0.0,
                                      "Development",
                                      "Marks the end of invenory")
            
            test_item_material = Material("Soraxium",
                                          iconsts.ItemType.MATERIAL,
                                          0.1,
                                          0.1,
                                          iconsts.MaterialType.METAL,
                                          "Hardest metal")
            
            test_weapon = Weapon("The blade of test",
                                 iconsts.ItemType.WEAPON,
                                 1,
                                 2,
                                 25,
                                 10,
                                 20,
                                 5,
                                 iconsts.WeaponType.SWORD, iconsts.Handness.TWO_HANDED,
                                 "The first weapon ever created in the game - Why so weak?")
            
            test_armor = Armor("Small test armour",
                               iconsts.ItemType.ARMOR,
                               3,
                               1,
                               3,
                               2,
                               iconsts.ArmorType.SHOULDER,
                               "As big as a sword, but stretches like crazy.")

            assert self.player.pickup_item(test_item_quest_1)
            assert self.player.pickup_item(test_item_misc)
            assert self.player.pickup_item(test_item_consumable)
            assert self.player.pickup_item(test_weapon)
            assert self.player.pickup_item(test_armor)
            assert self.player.pickup_item(test_item_material)
            assert self.player.pickup_item(test_item_quest_2)
    
            dng_dim = (dungeon.height, dungeon.width)

            ie_sections = InterfaceSections()
            ie_sections.view_size = max(0, len(self.player.inventory.items))

            # Game loop
            while True:
                stdscr.clear()

                dialog_msg = [f"{action.id}. {action.description}" for action in reversed(self.available_actions)]

                GameInterface.draw_interface(stdscr, ie_sections, self.player, enemies, dng_dim, dialog_msg, self.log, self.log_cursor)

                key = stdscr.getch()
            
                if key == 27:  # ESC
                    ie_sections.reset_cursor()
                    break
                elif key in (ord("i"), ord("I")):
                    ie_sections.toggle_stats()
                elif key == ord('-'):
                    if self.log_cursor < len(self.log) - 1:
                        self.log_cursor += 1
                elif key == ord('+'):
                    if self.log_cursor > 0:
                        self.log_cursor -= 1
                elif key in (ord('p'), ord("P")):
                    ie_sections.toggle_equipment()
                elif key in (ord('o'), ord("O")):
                    ie_sections.toggle_inventory()
                elif key == curses.KEY_DOWN and ie_sections.show_inventory:
                    ie_sections.inventory_cursor = min(ie_sections.inventory_cursor + 1, ie_sections.view_size - 1)
                    ie_sections.cursor_traversing_forward = True
                elif key == curses.KEY_UP and ie_sections.show_inventory:
                    ie_sections.inventory_cursor = max(0, ie_sections.inventory_cursor - 1)
                    ie_sections.cursor_traversing_forward = False
                elif key in (ord('f'), ord('F')) and ie_sections.show_inventory:
                     ie_sections.reset_cursor()
                     ie_sections.switch_inventory_view()
                else: #TODO Only on player action. Currently any key ticks
                    self.tick(key, dungeon, enemies)
                
                self.available_actions.clear()
                dialog_msg.clear()
                self.check_neighboors(dungeon)

                if self.eval_game_conditions(stdscr, enemies):
                    break

        curses.wrapper(main)

    def handle_logs(self, messages):
        if not messages:
            return

        if not isinstance(messages, list):
            messages = [messages]

        messages.reverse()

        for msg in messages:
            self.add_log(msg)

    def try_move(self, dy, dx, dungeon):
        old_y, old_x = self.player.position_y, self.player.position_x
        new_y, new_x = old_y + dy, old_x + dx

        message = dungeon.move_entity(self.player, new_y, new_x)
        if message:
            return message
                
        self.player.position_y, self.player.position_x = new_y, new_x  

    def add_log(self, message):
        log_cache_size = 100
        self.log.insert(0, message)
        if len(self.log) > log_cache_size:
            self.log.pop()

    def add_dialog_action(self, action):
        maximum_action_count = 9
        if len(self.available_actions) >= maximum_action_count:
            print("Cannot add more than 9 dialog actions!")
            return
        self.available_actions.insert(0, action)
            
    def check_neighboors(self, dungeon):
        py, px = self.player.position_y, self.player.position_x
        for dy, dx in mconsts.NEIGHBOR_CELLS:
            cell = dungeon.get_cell(py + dy, px + dx)
            if cell and cell.entity:
                self.evaluate_actor(cell.entity)

    def evaluate_actor(self, actor):
        name = actor.name
        action_count = len(self.available_actions)
        if actor.alignment in (econsts.Alignment.HOSTILE, econsts.Alignment.NEUTRAL):
            action = Action(action_count + 1,
                            f"Attack {name}",
                            partial(Combat.melee_attack, self.player, actor)
        )
        self.add_dialog_action(action)

    def actor_management(self, enemies, dungeon):
        log_messages = []
        for actor in enemies[:]:  # iterate over a shallow copy
            if not actor.is_alive():
                log_messages.append(f"{actor.name} died.")
                dungeon.remove_entity(actor, actor.position_y, actor.position_x)
                enemies.remove(actor)
            else:
                msg = actor.behavior(self.player, dungeon)
                if msg:
                    log_messages.extend(msg if isinstance(msg, list) else [msg])

        return log_messages
    
    def tick(self, key, dungeon, enemies):
        log_msg = None
        if key == curses.KEY_UP:
                log_msg = self.try_move(-1, 0, dungeon)
        elif key == curses.KEY_DOWN:
                log_msg = self.try_move(1, 0, dungeon)
        elif key == curses.KEY_LEFT:
                log_msg = self.try_move(0, -1, dungeon)
        elif key == curses.KEY_RIGHT:
                log_msg = self.try_move(0, 1, dungeon)
        elif key in (ord("1"), ord("2"), ord("3"),
                    ord("4"), ord("5"), ord("6"),
                    ord("7"), ord("8"), ord("9")):
                    action_id = int(chr(key))
                    for action in self.available_actions:
                        if action.id == action_id:
                            log_msg = action.execute()

        actor_logs = self.actor_management(enemies, dungeon)

        self.handle_logs(log_msg)
        self.handle_logs(actor_logs)

    def eval_game_conditions(self, stdscr, enemies):
        if not self.player.is_alive():
            stdscr.clear()
            go_text = ["YOU DIED", "GAME OVER"]
            GameInterface.draw_game_over(stdscr, go_text)
            stdscr.getch()
            return True
                
        if len(enemies) == 0:
            stdscr.clear()
            go_text = ["ALL ENEMIES ARE DEAD", "YOU ARE WINNER"]
            GameInterface.draw_game_over(stdscr, go_text)
            stdscr.getch()
            return True