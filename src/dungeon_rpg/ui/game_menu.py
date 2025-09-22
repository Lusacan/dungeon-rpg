from dungeon_rpg.game_rules.character_creator import CharacterCreator

class GameMenu:
    """
    Presents the available choices the player can take to control the game.
    """
    def __init__(self):
        print("Welcome to Dungeon RPG!\n")

    def start_new_game(self):
        print("\nCreate your character!")
        charcter_generator = CharacterCreator()
        player = charcter_generator.player_character
        print(repr(player))
        # TODO: Character creation -> generate dungeon

    def load_game(self):
        print("Select saved game:\n")
        # TODO: Load game from save file

    def settings(self):
        print("Settings menu\n")
        # TODO: Configuration menu

    def exit_game(self):
        print("Exiting game ...")
        exit(0)

    def display(self):
        menu_options = {
            "1": self.start_new_game,
            "2": self.load_game,
            "3": self.settings,
            "4": self.exit_game,
        }

        while True:
            print("Main Menu\n")
            for key, method in menu_options.items():
                print(f"{key}. {method.__name__.replace('_', ' ').title()}")

            choice = input("\nChoose an option: \n").strip()
            action = menu_options.get(choice)

            if action:
                action()
            else:
                print("Invalid choice! Select from available options.\n")