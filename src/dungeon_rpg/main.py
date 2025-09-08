from dungeon_rpg.ui.window import Window
from dungeon_rpg.entities import prime_entity
from dungeon_rpg.map import dungeon
from dungeon_rpg.game_rules.combat import Combat 
import time
import random

def main():
    print("Welcome to Dungeon RPG!")

    player = prime_entity.Entity(14, 14, 14, 11, 11, 11, 5, "P")
    enemy = prime_entity.Entity(5, 5, 5, 5, 5, 5, 2, "E")

    d = dungeon.Dungeon(10, 10)

    d.place_entity(player, 4, 6)
    d.place_entity(enemy, 6, 6)

    # print(d)

    d.move_entity(player, 5, 6)
    #print()
    #print(d)

    while enemy.is_alive():
        attack_roll = random.randint(1, 100)
        damage_roll = random.randint(1, player.damage)
        log1 = Combat.melee_attack(player, enemy, attack_roll, damage_roll)
        print(log1)
        if enemy.is_alive():
            e_attack_roll = random.randint(1, 100)
            e_damage_roll = random.randint(1, enemy.damage)
            log2 = Combat.melee_attack(enemy, player, e_attack_roll, e_damage_roll)
            print(log2)

        time.sleep(1)
        #print(player)
        #print(enemy)
        print()

    #mainWindow = Window()
    #mainWindow.on_execute()


if __name__ == "__main__":
    main()
