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

            test_item1 = Item("Book of revelation", iconsts.ItemType.MISC, 0.0, 0.0, "It contains the secrets of the universe")
            test_item2 = Item("Potion of health", iconsts.ItemType.CONSUMABLE, 0.1, 0.1, "Restore 5 healthpoint")
            test_item3 = Item("First item", iconsts.ItemType.QUEST, 0.1, 0.1, "Marks the beginning of inventory")
            test_item4 = Item("Last item", iconsts.ItemType.QUEST, 0.0, 0.0, "Marks the end of invenory")

            self.player.pickup_item(test_item3)
            i = 0
            while i < 20:
                self.player.pickup_item(test_item1)
                self.player.pickup_item(test_item2)
                i += 1
            self.player.pickup_item(test_item4)
            
            dng_dim = (dungeon.height, dungeon.width)

            ie_sections = InterfaceSections()

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
                        max_cursor = max(0, len(self.player.inventory.items))
                        ie_sections.inventory_cursor = min(ie_sections.inventory_cursor + 1, max_cursor - 1)
                        ie_sections.cursor_traversing_forward = True
                elif key == curses.KEY_UP and ie_sections.show_inventory:
                        ie_sections.inventory_cursor = max(0, ie_sections.inventory_cursor - 1)
                        ie_sections.cursor_traversing_forward = False
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