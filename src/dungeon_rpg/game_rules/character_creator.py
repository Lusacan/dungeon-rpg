import curses
import os
from dungeon_rpg.entities.player import Player
import dungeon_rpg.entities.constants as econst

class CharacterCreator:
    """
    This class is used to generate the player character
    """
    def __init__(self):
        self.race = self.race_selector()
        self.attributes = self.distribute_attribute_points()
        self.player_character = self.create_player_character(self.attributes)

    def race_selector(self):
        def main(stdscr):
            curses.curs_set(0)
            stdscr.nodelay(False)
            stdscr.keypad(True)
            cursor = 0

            while True:
                stdscr.clear()
                stdscr.addstr(0, 0, "Please select race! Use ↑/↓ to move or press i for information.\n")
                stdscr.addstr(1, 0, "Available races:\n")
                for i, race in enumerate(econst.available_races):
                    marker = ">" if i == cursor else " "
                    stdscr.addstr(i + 2, 0, f"{marker} {race.name.title()}.\n")

                stdscr.refresh()
                key = stdscr.getch()

                if key == curses.KEY_UP:
                    cursor = (cursor - 1) % len(econst.available_races)
                elif key == curses.KEY_DOWN:
                    cursor = (cursor + 1) % len(econst.available_races)
                elif key in (curses.KEY_ENTER, 10, 13):
                    selected_race = econst.available_races[cursor]
                    while True:
                        stdscr.addstr(len(econst.available_races)+3, 0, f"Selected race: {selected_race.name.title()}\n")
                        stdscr.addstr(len(econst.available_races)+4, 0, "Press enter to confirm or c to reselect.\n")
                        stdscr.refresh()
                        confirm_key = stdscr.getch()
                        if confirm_key in (curses.KEY_ENTER, 10, 13):
                            return selected_race
                        elif confirm_key in (ord("c"), ord("C")):
                            break
                        else:
                            stdscr.addstr(len(econst.available_races)+5, 0, "Invalid key. Press Enter or c/C.\n")
                            stdscr.refresh()
                            continue
                elif key in (ord("i"), ord("I")):
                    info_str = self.show_race_info(econst.available_races[cursor])
                    stdscr.addstr(len(econst.available_races)+3, 0, info_str)
                    stdscr.refresh()
                    stdscr.getch()  # wait for user to press a key
        return curses.wrapper(main)

    def show_race_info(self, race):
        info = econst.race_info.get(race)
        if info is not None:
            return info.get("description", "No description available.")
        return "No description available."

    def distribute_attribute_points(self):
        def main(stdscr):
            attributes = {
            "Strength": 0,
            "Dexterity": 0,
            "Endurance": 0, 
            "Intelligence": 0,
            "Willpower": 0,
            "Charisma": 0
            }
        
            self.apply_race_modifiers(attributes)

            curses.curs_set(0)  # hide cursor
            stdscr.nodelay(False)  # wait for user input
            stdscr.keypad(True)  # enable arrow keys

            available = econst.starting_attribute_points
            cursor = 0
            error_message = ""

            while True:
                stdscr.clear()
                stdscr.addstr(0, 0,
                              "You have 81 points to distribute amongst the six main attributes.\n"
                              "Each attribute must have a minimum value of 8 and a maximum value of 20.\n")
                stdscr.addstr(2, 0, f"Available points: {available}\n")
                stdscr.addstr(3, 0, "Use ↑/↓ to move, +/- to modify, F to finish.\n")

                for i, (attr, val) in enumerate(attributes.items()):
                    marker = ">" if i == cursor else " "
                    stdscr.addstr(i + 4, 0, f"{marker} {attr}: {val}")

                if error_message:
                    stdscr.addstr(12, 0, error_message)

                stdscr.refresh()
                key = stdscr.getch()

                if key == curses.KEY_UP:
                    cursor = (cursor - 1) % len(attributes)
                elif key == curses.KEY_DOWN:
                    cursor = (cursor + 1) % len(attributes)
                elif key in (ord("+"), ord("=")) and available > 0:
                    attr_name = list(attributes.keys())[cursor]
                    if attributes[attr_name] < 20:
                        attributes[attr_name] += 1
                        available -= 1
                elif key == ord("-"):
                    attr_name = list(attributes.keys())[cursor]
                    if attributes[attr_name] > 8:
                        attributes[attr_name] -= 1
                        available += 1
                elif key in (ord("f"), ord("F")):
                    if all(val >= 8 for val in attributes.values()):
                        if available == 0:
                            return attributes
                        else:
                            error_message = "You have unspent attribute points!"
                    else:
                        error_message = "All attributes must be at least 8!"

        return curses.wrapper(main)

    def apply_race_modifiers(self, attributes):
        modifiers = econst.race_info[self.race]["modifiers"]
        for attr, change in modifiers.items():
            attributes[attr] += change

    def create_player_character(self, attributes):
        def main(stdscr):
            curses.curs_set(1)  # show cursor while typing
            stdscr.clear()
            stdscr.addstr(0, 0, "Name your character (press Enter to confirm):\n")

            id = 0.07
            damage = 8
            name = ""
            while True:
                stdscr.addstr(1, 0, f"> {name}")
                stdscr.clrtoeol()
                stdscr.refresh()

                key = stdscr.getch()

                if key in (curses.KEY_ENTER, 10, 13):
                    if name.strip():
                        break
                elif key in (curses.KEY_BACKSPACE, 127, 8):
                    name = name[:-1]
                elif 32 <= key <= 126:
                    name += chr(key)

            curses.curs_set(0)

            new_player = Player(attributes["Strength"],
                                attributes["Dexterity"],
                                attributes["Endurance"],
                                attributes["Intelligence"],
                                attributes["Willpower"],
                                attributes["Charisma"],
                                damage,
                                id,
                                self.race.name.title(),
                                name)
            return new_player
        
        return curses.wrapper(main)
