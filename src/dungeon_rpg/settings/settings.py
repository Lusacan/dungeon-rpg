import curses
import sys
from dungeon_rpg.settings.constants import Interface 

class Settings:
     @staticmethod
     def check_terminal_size(min_rows=Interface.HEIGHT, min_cols=Interface.WIDTH):
        def _check(stdscr):
            interface_overhead = 10
            rows, cols = stdscr.getmaxyx()
            if rows < min_rows or cols < min_cols:
                stdscr.clear()
                msg = (f"Terminal too small! Needs at least "
                       f"{min_cols + interface_overhead}x{min_rows + interface_overhead}. "
                       "Resize and press any key.")
                stdscr.addstr(0, 0, msg)
                stdscr.refresh()
                stdscr.getch()
                return False
            return True

        curses.wrapper(_check)

    #TODO: Handle terminal size change -> Modify interface boxes ratios