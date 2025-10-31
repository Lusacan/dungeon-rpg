from dungeon_rpg.inventory_and_equipment.equipment_slot import Slot
import dungeon_rpg.inventory_and_equipment.constants as ieconsts

class Equipment:
    def __init__(self):
        self.armour_slots = {
            ieconsts.EquipmentSlot.HEAD: Slot(ieconsts.EquipmentSlot.HEAD),
            ieconsts.EquipmentSlot.SHOULDER: Slot(ieconsts.EquipmentSlot.SHOULDER),
            ieconsts.EquipmentSlot.TORSO: Slot(ieconsts.EquipmentSlot.TORSO),
            ieconsts.EquipmentSlot.BRACE: Slot(ieconsts.EquipmentSlot.BRACE),
            ieconsts.EquipmentSlot.FEET: Slot(ieconsts.EquipmentSlot.FEET),
            ieconsts.EquipmentSlot.LEGS: Slot(ieconsts.EquipmentSlot.LEGS),
            ieconsts.EquipmentSlot.HANDS: Slot(ieconsts.EquipmentSlot.HANDS)
        }

        self.weapon_slots = {
            ieconsts.EquipmentSlot.LEFT_HAND : Slot(ieconsts.EquipmentSlot.LEFT_HAND),
            ieconsts.EquipmentSlot.RIGHT_HAND : Slot(ieconsts.EquipmentSlot.RIGHT_HAND),
            ieconsts.EquipmentSlot.QUIVER : Slot(ieconsts.EquipmentSlot.QUIVER)
        }

        self.weight_sum = 0

    def equip_item(self, item):
        itype = item.item_type
        previous = None
        if itype == ieconsts.ItemType.WEAPON:
            previous = self.equip_weapon(item)
        elif itype == ieconsts.ItemType.ARMOR:
            previous = self.equip_armor(item)
        
        self.weight_sum += item.weight
        if previous:
            self.weight_sum -= previous.weight
        return previous

    def equip_weapon(self, weapon):
        previous = None
        wtype = weapon.weapon_type
        weapon_slot_left = self.weapon_slots[ieconsts.EquipmentSlot.LEFT_HAND]
        weapon_slot_right = self.weapon_slots[ieconsts.EquipmentSlot.RIGHT_HAND]
        if wtype == ieconsts.WeaponType.SHIELD:
            previous = weapon_slot_right.item
            weapon_slot_right.equip(weapon)
        elif wtype == ieconsts.WeaponType.QUIVER:
            quiver_slot = self.weapon_slots[ieconsts.EquipmentSlot.QUIVER]
            previous = quiver_slot.item
            quiver_slot.equip(weapon)
        else:
            lr_hand = weapon.handness
            if lr_hand == ieconsts.Handness.ONE_HANDED:
                if weapon_slot_left.occupied:
                    previous = weapon_slot_right.item
                    weapon_slot_right.equip(weapon)
                else:
                    previous = weapon_slot_left.item
                    weapon_slot_left.equip(weapon)
            else:
                previous = weapon_slot_left.item
                weapon_slot_left.equip(weapon)
                weapon_slot_right.set_occupied()
        return previous

    def equip_armor(self, armor):
        slot = self.armour_slots.get(ieconsts.EquipmentSlot[armor.armor_type.name])
        previous = None
        if slot:
            previous = slot.item
            slot.equip(armor)
        return previous
        
    def unequip_item(self, slot):
        to_inventory = None
        if slot.item:
            to_inventory = slot.item
            self.weight_sum -= slot.item.weight
            slot.unequip()
        return to_inventory
