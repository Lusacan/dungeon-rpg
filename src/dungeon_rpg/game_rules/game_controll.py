import curses
from functools import partial
import dungeon_rpg.entities.constants as econsts 
from dungeon_rpg.game_rules.combat import Combat
from dungeon_rpg.ui.game_interface import GameInterface
from dungeon_rpg.map.dungeon_generator import DungeonGenerator
import dungeon_rpg.map.constants as mconsts
from dungeon_rpg.entities.actor_generator import ActorGenerator
from dungeon_rpg.game_rules.action import Action
from dungeon_rpg.settings.settings import Settings

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

            enemies = self.actor_generator.generate_actors(dungeon,
                                             econsts.EntityType.HUMANOID,
                                             econsts.Alignment.HOSTILE,
                                             "Goblin")

            self.player.position_x = 0
            self.player.position_y = 0
            dungeon.place_entity(self.player, self.player.position_y, self.player.position_x)
            
            show_stats = False

            dng_dim = (dungeon.height, dungeon.width)

            # Game loop
            while True:
                stdscr.clear()
                
                inf_str = f"Welcome to the dungeon {self.player.name}! Defeat enemies and find the entrance to the next level.\nEsc - Menu, I - Stats, ↑/↓ ←/→ - Move"
                if show_stats:  
                    inf_str += f"\nPlayer stats: {self.player}"

                log_msg = ""

                dialog_msg = [f"{action.id}. {action.description}" for action in reversed(self.available_actions)]

                player_loc = (self.player.position_y ,self.player.position_x)

                GameInterface.draw_interface(stdscr, player_loc, enemies, dng_dim, inf_str, dialog_msg, self.log, self.log_cursor)

                key = stdscr.getch()
            
                if key == 27:  # ESC
                    break
                elif key in (ord("i"), ord("I")):
                    show_stats = not show_stats
                elif key == ord('-'):
                    if self.log_cursor < len(self.log) - 1:
                        self.log_cursor += 1
                elif key == ord('+'):
                    if self.log_cursor > 0:
                        self.log_cursor -= 1
                else:
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
            actor = dungeon.get_cell(py + dy, px + dx)
            if actor:
                self.evaluate_actor(actor)

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