import curses
import textwrap
import logging
from typing import Optional
from dataclasses import dataclass
import dungeon_rpg.settings.constants as sconsts
import dungeon_rpg.inventory_and_equipment.constants as iconsts
from dungeon_rpg.ui.messages import UIMessages
from dungeon_rpg.entities.player import Player
import dungeon_rpg.entities.constants as econsts
from dungeon_rpg.inventory_and_equipment.item import Item
from dungeon_rpg.inventory_and_equipment.equipment_slot import Slot

logging.basicConfig(
    filename="interface.log",          # file to write logs
    filemode="w",                 # "a" for append, "w" for overwrite
    level=logging.DEBUG,          # minimum log level
    format="%(asctime)s [%(levelname)s] %(message)s"
)

@dataclass
class InterfaceSections:
    show_infobox : bool = True
    show_stats: bool = False
    show_dialogbox : bool = True
    show_dungeonbox : bool = True
    show_logbox : bool = True
    show_equipment : bool = False
    show_inventory : bool = False
    inventory_view : sconsts.InventoryView = sconsts.InventoryView.DEFAULT
    inventory_ordering = sconsts.InventoryOrdering = sconsts.InventoryOrdering.DEFAULT
    view_size : int = 0

    inventory_cursor = 0
    cursor_traversing_forward : bool = False

    def toggle_inventory(self):
        if self.show_equipment:
            self.toggle_equipment()
        self.inventory_cursor = 0
        self.show_inventory = not self.show_inventory
        self.show_dialogbox = not self.show_dialogbox
        self.show_dungeonbox = not self.show_dungeonbox

    def toggle_equipment(self):
        if self.show_inventory:
            self.toggle_inventory()
        self.inventory_cursor = 0
        self.show_equipment = not self.show_equipment
        self.show_dialogbox = not self.show_dialogbox
        self.show_dungeonbox = not self.show_dungeonbox

    def toggle_stats(self):
        self.show_stats = not self.show_stats

    def reset_cursor(self):
        self.inventory_cursor = 0

    def switch_inventory_view(self):
        """Cycle to the next inventory view."""
        views = list(sconsts.InventoryView)
        current_index = views.index(self.inventory_view)
        next_index = (current_index + 1) % len(views)
        self.inventory_view = views[next_index]
        self.reset_cursor()

@dataclass
class InterfaceSelections:
    selected_item: Optional[Item] = None
    slot_to_unequip: Optional[Slot] = None

@dataclass
class BoxLayout:
    start_line: int
    start_column: int
    height: int
    width: int
    title: str = ""

@dataclass
class InterfaceLayout:
    info_box: BoxLayout
    dialog_box: BoxLayout
    dungeon_box: BoxLayout
    log_box: BoxLayout
    equipment_box: BoxLayout
    inventory_box: BoxLayout
    description_box: BoxLayout
    player_stats_box: BoxLayout

class GameInterface:
    inventory_start_index = 0
    inventory_end_index = sconsts.Inventory.available_lines

    @staticmethod
    def draw_interface(stdscr,
                       ie_sections,
                       ie_selections,
                       player,
                       enemies,
                       dng_dim,
                       dialog_context,
                       log_context,
                       log_cursor):
        interface_width = sconsts.Interface.WIDTH
        info_box_height = sconsts.Interface.INFO_BOX_HEIGHT
        dialog_box_height = sconsts.Interface.DIALOG_BOX_HEIGHT
        dialog_box_width = sconsts.Interface.DIALOG_BOX_WIDTH
        dungeon_box_width = sconsts.Interface.DUNGEON_BOX_WIDTH
        dungeon_box_height = sconsts.Interface.DUNGEON_BOX_HEIGHT
        dungeon_box_posX = (interface_width // 2) - (dungeon_box_width // 2)
        equipment_box_height = sconsts.Interface.EQUIPMENT_BOX_HEIGHT
        equipment_box_width = sconsts.Interface.EQUIPMENT_BOX_WIDTH
        inventroy_box_height = equipment_box_height
        inventroy_box_width = equipment_box_width
        description_box_posY = interface_width - sconsts.Interface.DESCRIPTION_BOX_WIDTH
        log_box_height = sconsts.Interface.LOG_BOX_HEIGHT
        log_box_width = sconsts.Interface.LOG_BOX_WIDTH
        log_box_posY = info_box_height + dungeon_box_height + sconsts.Interface.DUNGEON_BOX_PADDING_HEIGHT

        player_location = (player.position_y, player.position_x)
        
        layout = InterfaceLayout(
            info_box=BoxLayout(0, 0, info_box_height, interface_width, "Info"),
            dialog_box=BoxLayout(info_box_height, 0, dialog_box_height, dialog_box_width, "Dialog"),
            dungeon_box=BoxLayout(info_box_height, dungeon_box_posX, dungeon_box_height, dungeon_box_width, "Dungeon"),
            log_box=BoxLayout(log_box_posY, 0, log_box_height, log_box_width, "Log"),
            equipment_box=BoxLayout(info_box_height, 0, equipment_box_height, equipment_box_width, "Equipment"),
            inventory_box=BoxLayout(info_box_height, 0, inventroy_box_height, inventroy_box_width, "Inventory"),
            description_box=BoxLayout(info_box_height,
                                      description_box_posY,
                                      inventroy_box_height,
                                      sconsts.Interface.DESCRIPTION_BOX_WIDTH,
                                      "Description"),
            player_stats_box=BoxLayout(info_box_height,
                                      description_box_posY,
                                      inventroy_box_height,
                                      sconsts.Interface.DESCRIPTION_BOX_WIDTH,
                                      "Statistics"),
        )

        inf_str = GameInterface.construct_info_str(ie_sections, player)

        if ie_sections.show_infobox:
            GameInterface.draw_info_box(stdscr, layout.info_box, inf_str)
        
        if ie_sections.show_dialogbox:
            GameInterface.draw_dialog_box(stdscr, layout.dialog_box, dialog_context)

        if ie_sections.show_equipment:
            GameInterface.draw_equipment_box(stdscr,
                                             layout.equipment_box,
                                             layout.player_stats_box,
                                             player,
                                             ie_sections,
                                             ie_selections)
            
        if ie_sections.show_inventory:
            GameInterface.draw_inventory_box(stdscr,
                                             layout.inventory_box,
                                             layout.description_box,
                                             player,
                                             ie_sections,
                                             ie_selections)
        
        if ie_sections.show_dungeonbox:
            GameInterface.draw_dungeon_box(stdscr,
                                        layout.dungeon_box,
                                        dng_dim,
                                        player_location,
                                        enemies)

        if ie_sections.show_logbox:
            GameInterface.draw_log_box(stdscr,
                                       layout.log_box,
                                       log_context,
                                       log_cursor)
            
    def construct_info_str(ie_sections: InterfaceSections, player: Player):
        inf_str = ""
        if ie_sections.show_equipment == False and ie_sections.show_inventory == False:
            inf_str = UIMessages.WELCOME.format(player_name=player.name)
            if ie_sections.show_stats:
                inf_str += f"\nPlayer stats: {player}"

        if ie_sections.show_inventory:
            inf_str = UIMessages.INVENTORY
            max_size = player.inventory.max_capacity
            curr_size = player.inventory.current_size
            max_load = player.inventory.max_load
            curr_load = player.inventory.current_weight
            inf_str += f"\nCapacity: {curr_size}/{max_size}, Load: {curr_load}/{max_load}"

        if ie_sections.show_equipment:
            inf_str = UIMessages.EQUIPMENT

        return inf_str
        
    def draw_game_over(stdscr, go_text):
        go_height = sconsts.Interface.HEIGHT
        go_width = sconsts.Interface.WIDTH

        GameInterface.draw_box(stdscr, 0, 0, go_height, go_width)

        start_y = go_height // 2 - len(go_text) // 2

        for i, line in enumerate(go_text):
            start_x = (go_width - len(line)) // 2
            stdscr.addstr(start_y + i, start_x, line)

    def draw_info_box(stdscr, layout: BoxLayout, text: str):
        GameInterface.draw_box(stdscr,
                               layout.start_line,
                               layout.start_line,
                               layout.height,
                               layout.width,
                               title=layout.title)
        
        GameInterface.draw_text_in_box(stdscr,
                                       layout.start_line,
                                       layout.start_column,
                                       layout.height,
                                       layout.width,
                                       text)

    def draw_dialog_box(stdscr, layout: BoxLayout, dialog_box_context):
        GameInterface.draw_box(stdscr,
                               layout.start_line,
                               layout.start_column,
                               layout.height,
                               layout.width,
                               title=layout.title)
        
        start_column = 1
        for i, line in enumerate(dialog_box_context):
            if i >= layout.height - 2:
                break
            stdscr.addstr(layout.start_line + 1 + i, start_column, line)

    def draw_equipment_box(stdscr,
                           equip_layout: BoxLayout,
                           stat_layout: BoxLayout,
                           player: Player,
                           ie_sections: InterfaceSections,
                           ie_selections: InterfaceSelections):
        GameInterface.draw_box(stdscr,
                               equip_layout.start_line,
                               equip_layout.start_column,
                               equip_layout.height,
                               equip_layout.width,
                               equip_layout.title)
        
        columns = sconsts.Equipment.equipment_column_names

        GameInterface.draw_equipment_table(stdscr, 
                                           equip_layout.start_line + 1,
                                           equip_layout.start_column + 1,
                                           columns)
        
        GameInterface.fill_equipment_table(stdscr,
                                           equip_layout.start_line + 2,
                                           equip_layout.start_column + 1,
                                           columns,  
                                           player,
                                           ie_sections,
                                           ie_selections)
        
        GameInterface.draw_box(stdscr,
                               stat_layout.start_line,
                               stat_layout.start_column,
                               stat_layout.height,
                               stat_layout.width,
                               stat_layout.title)
        
        player_statistics = GameInterface.generate_statistics(player)

        GameInterface.draw_text_in_box(stdscr,
                                       stat_layout.start_line,
                                       stat_layout.start_column,
                                       stat_layout.height,
                                       stat_layout.width,
                                       player_statistics)

    def draw_inventory_box(stdscr,
                           inv_layout: BoxLayout,
                           desc_layout: BoxLayout,
                           player: Player,
                           ie_sections: InterfaceSections,
                           ie_selections: InterfaceSelections):
        GameInterface.draw_box(stdscr,
                               inv_layout.start_line,
                               inv_layout.start_column,
                               inv_layout.height,
                               inv_layout.width,
                               inv_layout.title)
        
        columns = None
        if ie_sections.inventory_view == sconsts.InventoryView.DEFAULT:
            columns = sconsts.Inventory.default_colum_names
        elif ie_sections.inventory_view == sconsts.InventoryView.WEAPONS:
            columns = sconsts.Inventory.weapon_column_names
        elif ie_sections.inventory_view == sconsts.InventoryView.ARMORS:
            columns = sconsts.Inventory.armor_column_names
        elif ie_sections.inventory_view == sconsts.InventoryView.CONSUMABLES:
            columns = sconsts.Inventory.consumables_column_names
        elif ie_sections.inventory_view == sconsts.InventoryView.MATERIALS:
            columns = sconsts.Inventory.material_column_names
        elif ie_sections.inventory_view == sconsts.InventoryView.QUESTS:
            columns = sconsts.Inventory.quest_column_names
        elif ie_sections.inventory_view == sconsts.InventoryView.MISCS:
            columns = sconsts.Inventory.misc_column_names
        
        GameInterface.draw_inventory_table(stdscr, 
                                           inv_layout.start_line + 1,
                                           inv_layout.start_column + 1,
                                           columns)
        filtered_items = GameInterface.fill_inventory_table(stdscr,
                                           inv_layout.start_line + 2,
                                           inv_layout.start_column + 1,
                                           columns,
                                           player,
                                           ie_sections)
        
        GameInterface.draw_box(stdscr,
                               desc_layout.start_line,
                               desc_layout.start_column,
                               desc_layout.height,
                               desc_layout.width,
                               desc_layout.title)
        
        #if ie_sections.inventory_cursor >= len(filtered_items):
         #   ie_sections.inventory_cursor = max(0, len(filtered_items) - 1)
            
        ie_selections.selected_item = filtered_items[ie_sections.inventory_cursor]
        item_description = ie_selections.selected_item.description

        GameInterface.draw_text_in_box(stdscr,
                                       desc_layout.start_line,
                                       desc_layout.start_column,
                                       desc_layout.height,
                                       desc_layout.width,
                                       item_description)

    def draw_dungeon_box(stdscr,
                         layout: BoxLayout,
                         dungeon_dimensions,
                         player_location,
                         enemies):
        # Set position aligment to middle of the interface
        dungeon_height, dungeon_width = dungeon_dimensions
        player_loc_y, player_loc_x = player_location

        dungeon_grid = [[" " for _ in range(dungeon_width)] for _ in range(dungeon_height)]
        dungeon_grid[player_loc_y][player_loc_x] = sconsts.Symbols.PLAYER

        for enemy in enemies:
            e_pos_y = enemy.position_y
            e_pos_x = enemy.position_x
            dungeon_grid[e_pos_y][e_pos_x] = str(enemy.id)

        dungeon_box_height = layout.height + sconsts.Interface.DUNGEON_BOX_PADDING_HEIGHT
        dungeon_box_width = layout.width + sconsts.Interface.DUNGEON_BOX_PADDING_WIDTH

        GameInterface.draw_box(stdscr,
                               layout.start_line,
                               layout.start_column,
                               dungeon_box_height,
                               dungeon_box_width,
                               title=layout.title)

        GameInterface.draw_dungeon_grid(stdscr,
                                        layout.start_line,
                                        layout.start_column,
                                        dungeon_box_height - 2, #MINUS PADDING
                                        dungeon_box_width - 2,
                                        dungeon_height,
                                        dungeon_width,
                                        dungeon_grid)
        
        
    def draw_log_box(stdscr, layout: BoxLayout, log_context, log_cursor):
        GameInterface.draw_box(stdscr,
                               layout.start_line,
                               layout.start_column,
                               layout.height,
                               layout.width,
                               title=layout.title)
        
        visible_logs = log_context[log_cursor:log_cursor + layout.height - 2]

        for i, line in enumerate(visible_logs):
            stdscr.addstr(layout.start_line + 1 + i,
                          layout.start_column + 2,
                          line)


    def draw_box(stdscr, top, left, height, width, title=""):
        max_y, max_x = stdscr.getmaxyx()
        if height > max_y or width > max_x:
            raise ValueError(f"Terminal too small: need {height}x{width}, got {max_y}x{max_x}")
    # Draw top and bottom borders
        for x in range(width):
            stdscr.addstr(top, left + x, "-")                   # top
            stdscr.addstr(top + height - 1, left + x, "-")      # bottom

        # Draw left and right borders
        for y in range(1, height - 1):
            stdscr.addstr(top + y, left, "|")                   # left
            stdscr.addstr(top + y, left + width - 1, "|")       # right

        # Draw corners
        stdscr.addstr(top, left, "+")
        stdscr.addstr(top, left + width - 1, "+")
        stdscr.addstr(top + height - 1, left, "+")
        stdscr.addstr(top + height - 1, left + width - 1, "+")

        # Optional title
        if title:
            stdscr.addstr(top, left + 2, f"[ {title} ]")


    def draw_text_in_box(stdscr,
                         start_line,
                         start_column,
                         height,
                         width,
                         text):
        # Leave 1 character padding on each side
        max_width = width - 2
        lines = text.split("\n")  # preserve explicit newlines
        wrapped_lines = []

        for line in lines:
            if line == "EMPTY_LINE":
                wrapped_lines.append("")  # insert a blank line
            else:
                wrapped_lines.extend(textwrap.wrap(line, max_width))
    
        for i, line in enumerate(wrapped_lines):
            # Make sure we don't write outside the box height
            if i >= height - 2:
                break
            stdscr.addstr(start_line + 1 + i, start_column + 1, line)


    def draw_dungeon_grid(stdscr,
                          start_line,
                          start_column,
                          d_box_no_pad_height,
                          d_box_no_pad_width,
                          dungeon_height,
                          dungeon_width,
                          dungeon_grid):
        # Offsets so the dungeon is centered inside the inner area
        y_offset = (d_box_no_pad_height - dungeon_height) // 2
        x_offset = (d_box_no_pad_width - dungeon_width) // 2

        for y in range(d_box_no_pad_height):
            for x in range(d_box_no_pad_width):
                # Check if this is the dungeon playable space
                in_dungeon = (
                    y_offset <= y < y_offset + dungeon_height
                    and x_offset <= x < x_offset + dungeon_width
                )

                if in_dungeon:
                    # Calculate actual dungeon coordinates
                    dy = y - y_offset
                    dx = x - x_offset
                    ch = dungeon_grid[dy][dx]
                    stdscr.addstr(start_line + 1 + y, start_column + 1 + x, ch)
                else:
                    # Fill walls in padding layer
                    stdscr.addstr(start_line + 1 + y, start_column + 1 + x, "■")

    def draw_inventory_table(stdscr, start_line, start_column, column_names):
        current_x = start_column
        
        for i, (header, width) in enumerate(column_names):
            centered_name = header.center(width - 1)

            stdscr.addstr(start_line, current_x, centered_name)

            if i < len(column_names) - 1:
                for y in range(0, sconsts.Interface.EQUIPMENT_BOX_HEIGHT - 2):
                    stdscr.addstr(start_line + y, current_x + width - 1, "|")

            current_x += width

    def draw_equipment_table(stdscr, start_line, start_column, column_names):
        current_x = start_column
        
        for i, (header, width) in enumerate(column_names):
            centered_name = header.center(width - 1)

            stdscr.addstr(start_line, current_x, centered_name)

            if i < len(column_names) - 1:
                for y in range(0, sconsts.Interface.EQUIPMENT_BOX_HEIGHT - 2):
                    stdscr.addstr(start_line + y, current_x + width - 1, "|")

            current_x += width

    def fill_equipment_table(stdscr,
                             start_line,
                             start_column,
                             columns,
                             player: Player,
                             ie_sections: InterfaceSections,
                             ie_selections: InterfaceSelections):
        armor_slots = list(player.equipment.armour_slots.values())
        weapon_slots = list(player.equipment.weapon_slots.values())
        all_slots = armor_slots + weapon_slots
        row_y = start_line
        visible_rows = sconsts.Inventory.available_lines
        ie_sections.view_size = len(all_slots)

        #If inventory cursor was reseted reset visible items too
        if ie_sections.inventory_cursor == 0:
            GameInterface.inventory_start_index = 0
            GameInterface.inventory_end_index = min(ie_sections.view_size, visible_rows)

        for i, slot in enumerate(all_slots):
            current_x = start_column
            global_index = GameInterface.inventory_start_index + i

            if slot.occupied == True:
                if slot.item:
                    item_name = slot.item.name
                else:
                    item_name = iconsts.OCCUPIED
            else:
                item_name = iconsts.EMPTY_SLOT

            item_in_slot = [slot.slot_name, item_name]

            # Highlight if this line corresponds to the cursor’s item
            if global_index == ie_sections.inventory_cursor:
                attr = curses.A_REVERSE 
                ie_selections.slot_to_unequip = slot
            else:
                attr = curses.A_NORMAL

            for (header, width), value in zip(columns, item_in_slot):
                if header == "Slot":
                    text = value.ljust(width - 1)
                else:
                    text = value.center(width - 1)
                    
                stdscr.addstr(row_y, current_x, text, attr)
                current_x += width

            row_y += 1

    def generate_statistics(player: Player) -> str:
        lines = []

        for group_name, attrs in econsts.stat_groups:
            for attr in attrs:
                value = getattr(player, attr)
                # Special formatting for max values
                if attr in ("health", "pain_tolerance"):
                    max_attr = "max_" + attr
                    max_value = getattr(player, max_attr)
                    lines.append(f"{attr.replace('_', ' ').title()}: {value}/{max_value}")
                else:
                    lines.append(f"{attr.replace('_', ' ').title()}: {value}")
            lines.append("EMPTY_LINE")  # insert an empty line between groups

        # Remove the last empty line for a cleaner look
        if lines and lines[-1] == "EMPTY_LINE":
            lines.pop()

        return "\n".join(lines)

    def filter_items(player: Player, ie_sections: InterfaceSections):
        """Return the items matching the current inventory view."""
        if ie_sections.inventory_view == sconsts.InventoryView.DEFAULT:
            logging.debug(f"Player Items: {player.inventory.items}")
            return player.inventory.items

        # Map InventoryView to ItemType
        view_to_type = {
            sconsts.InventoryView.WEAPONS: iconsts.ItemType.WEAPON,
            sconsts.InventoryView.ARMORS: iconsts.ItemType.ARMOR,
            sconsts.InventoryView.CONSUMABLES: iconsts.ItemType.CONSUMABLE,
            sconsts.InventoryView.MATERIALS: iconsts.ItemType.MATERIAL,
            sconsts.InventoryView.QUESTS: iconsts.ItemType.QUEST,
            sconsts.InventoryView.MISCS: iconsts.ItemType.MISC,
        }

        filter_type = view_to_type.get(ie_sections.inventory_view, None)
        if filter_type is None:
            return []  # fallback empty list

        return [item for item in player.inventory.items if item.item_type == filter_type]
    
    def order_by(ie_sections: InterfaceSections, items):
        ordering = ie_sections.inventory_ordering

        if ordering == sconsts.InventoryOrdering.NAME:
            return sorted(items, key=lambda item: item.name)
        
        if ordering == sconsts.InventoryOrdering.TYPE:
            return sorted(items, key=lambda item: item.type_name)
        
        if ordering == sconsts.InventoryOrdering.WEIGHT:
            return sorted(items, key=lambda item: item.weight)
        
        if ordering == sconsts.InventoryOrdering.VOLUME:
            return sorted(items, key=lambda item: item.volume)
        
        return items

    def fill_inventory_table(stdscr,
                             start_line,
                             start_column,
                             columns,
                             player: Player,
                             ie_sections: InterfaceSections):

        row_y = start_line
        visible_rows = sconsts.Inventory.available_lines
        items = GameInterface.filter_items(player, ie_sections)
        items = GameInterface.order_by(ie_sections, items)
        ie_sections.view_size = len(items)

        #TODO: Enable ordering by item properties on filters (weapon dmg, armor dr etc))
        if ie_sections.inventory_cursor >= len(player.inventory.items):
            ie_sections.inventory_cursor = max(0, len(player.inventory.items) - 1)

        #If inventory cursor was reseted reset visible items too
        if ie_sections.inventory_cursor == 0:
            GameInterface.inventory_start_index = 0
            GameInterface.inventory_end_index = min(ie_sections.view_size, visible_rows)

        # Move window if cursor goes out of visible range
        if ie_sections.inventory_cursor < GameInterface.inventory_start_index:
            GameInterface.inventory_start_index -= 1
            GameInterface.inventory_end_index -= 1
        elif ie_sections.inventory_cursor >= GameInterface.inventory_end_index:
            GameInterface.inventory_start_index += 1
            GameInterface.inventory_end_index += 1

        # Keep window within bounds
        if GameInterface.inventory_start_index < 0:
            GameInterface.inventory_start_index = 0
            GameInterface.inventory_end_index = visible_rows

        if GameInterface.inventory_end_index > ie_sections.view_size:
            GameInterface.inventory_start_index = max(0, ie_sections.view_size - visible_rows)
            GameInterface.inventory_end_index = ie_sections.view_size

        visible_items = items[
            GameInterface.inventory_start_index:GameInterface.inventory_end_index
        ]

        for i, item in enumerate(visible_items):
            current_x = start_column
            global_index = GameInterface.inventory_start_index + i

            if ie_sections.inventory_view == sconsts.InventoryView.DEFAULT:
                values = [
                    item.display_name,
                    item.type_name,
                    f"{item.weight:.1f}",
                    f"{item.volume:.1f}"
                ]
            elif ie_sections.inventory_view == sconsts.InventoryView.WEAPONS:
                values = [
                    str(item.name),
                    item.subtype_name,
                    item.handness_name,
                    f"{item.attack}",
                    f"{item.defense}",
                    f"{item.damage}",
                    f"{item.speed}"
                ]
            elif ie_sections.inventory_view == sconsts.InventoryView.ARMORS:
                values = [
                    str(item.name),
                    item.subtype_name,
                    f"{item.dav}",
                    f"{item.mrf}",
                ]
            elif ie_sections.inventory_view == sconsts.InventoryView.CONSUMABLES:
                values = [
                    str(item.name),
                    item.subtype_name,
                    f"{item.quantity}",
                ]
            elif ie_sections.inventory_view == sconsts.InventoryView.MATERIALS:
                values = [
                    str(item.name),
                    item.subtype_name,
                    f"{item.quantity}",
                ]
            elif ie_sections.inventory_view == sconsts.InventoryView.QUESTS:
                values = [
                    str(item.name),
                    item.type_name,
                    f"{item.quest_name}",
                ]
            elif ie_sections.inventory_view == sconsts.InventoryView.MISCS:
                values = [
                    str(item.name),
                    item.subtype_name,
                    f"{item.quantity}",
                ]
            
            # Highlight if this line corresponds to the cursor’s item
            attr = curses.A_REVERSE if global_index == ie_sections.inventory_cursor else curses.A_NORMAL

            for (header, width), value in zip(columns, values):
                if header == "Name":
                    text = value.ljust(width - 1)
                else:
                    text = value.center(width - 1)
                    
                stdscr.addstr(row_y, current_x, text, attr)
                current_x += width

            row_y += 1

        return items
    
    def underscore_header(text: str, width: int) -> str:
        text = f" {text} "
        if len(text) >= width:
            return text[:width]
        padding = width - len(text)
        left = padding // 2
        right = padding - left
        return "_" * left + text + "_" * right