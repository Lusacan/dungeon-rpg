from dungeon_rpg.ui.window import Window
from dungeon_rpg.entities import entity
from dungeon_rpg.map import dungeon_room
from dungeon_rpg.game_rules.combat import Combat 
from dungeon_rpg.ui.game_menu import GameMenu
import time
import random

def main():
    menu = GameMenu()
    menu.display()

    #mainWindow = Window()
    #mainWindow.on_execute()


if __name__ == "__main__":
    main()
