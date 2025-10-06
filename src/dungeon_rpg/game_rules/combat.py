class Combat():
    """
    Logic for attacks (melee, ranged) and wound system  
    """
    @staticmethod
    def melee_attack(attacker, defender, attack_roll=None, damage_roll=None):
        attack_log = []

        attack_log.append(f"{attacker.id} is attacking: {defender.id}. Attack roll: {attack_roll}")

        hp_damage = 0
        pt_damage = 0

        failure = False

        if attack_roll == 1:
            failure = True
            attack_log.append("Critical failure!")
        elif attack_roll == 100:
            attack_log.append("Critical hit!")
            hp_damage += 3
            pt_damage += 6

        attack_result = attack_roll + attacker.melee_attack
        defense = defender.melee_defense
        if not failure:

            if attack_result <= defense:
                attack_log.append("Miss!")
                return attack_log
            
            attack_log.append(f"Damage roll: {damage_roll}")

            if attack_result > defense + 50:
                hp_damage += damage_roll
                pt_damage += damage_roll * 2
                if defender.pain_tolerance == 0:
                    if defender.health <= hp_damage:
                        hp_damage = defender.health
                    attack_log.append(f"Overwhelming strike! {defender.id} loses {hp_damage} health.")
                elif pt_damage >= defender.pain_tolerance:
                    attack_log.append(f"Overwhelming strike! {defender.id} loses {hp_damage} health and {defender.pain_tolerance} pain tolerance.")
                else:
                    attack_log.append(f"Overwhelming strike! {defender.id} loses {hp_damage} health and {pt_damage} pain tolerance.")
                defender.take_damage(hp_damage, pt_damage)
            elif attack_result > defense:
                if defender.pain_tolerance == 0:
                    hp_damage += damage_roll
                    if defender.health <= hp_damage:
                        hp_damage = defender.health
                    attack_log.append(f"Hit! {defender.id} loses {hp_damage} health.")
                elif defender.pain_tolerance < damage_roll:
                    hp_damage += damage_roll - defender.pain_tolerance
                    pt_damage = defender.pain_tolerance
                    attack_log.append(f"Hit! {defender.id} loses {hp_damage} health and {pt_damage} pain tolerance.")
                else:
                    pt_damage += damage_roll
                    collateral_dmg = damage_roll // 5
                    hp_damage += collateral_dmg
                    if hp_damage > 0:
                        attack_log.append(f"Hit! {defender.id} loses {hp_damage} health and {pt_damage} pain tolerance.")
                    else:
                        attack_log.append(f"Hit! {defender.id} loses {pt_damage} pain tolerance.")
                    if collateral_dmg > 0:
                        attack_log.append(f"Collateral damage: {collateral_dmg}")
                defender.take_damage(hp_damage, pt_damage)
                
        else:
            attack_log.append(f"{attacker.id} fumbles the attack!")
        return attack_log
