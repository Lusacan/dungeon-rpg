import curses
import textwrap
import dungeon_rpg.settings.constants as sconsts

class GameInterface:
    @staticmethod
    def draw_interface(stdscr,
                       player_location,
                       enemies,
                       dungeon_dimensions,
                       info_context,
                       dialog_context,
                       log_context,
                       log_cursor):  
         
        interface_width = sconsts.Interface.WIDTH
        info_box_height = sconsts.Interface.INFO_BOX_HEIGHT
        info_box_width = interface_width
        dungeon_max_size = sconsts.Interface.DUNGEON_MAX_SIZE
        dungeon_box_padding = sconsts.Interface.DUNGEON_BOX_PADDING # 2 For box borders and 2 for walls
        dungeon_box_size = dungeon_max_size + dungeon_box_padding
        dialog_box_width = (interface_width // 2) - (dungeon_box_size // 2) - 1
        dialog_box_dimensions = (dungeon_box_size, dialog_box_width)
        log_box_height = sconsts.Interface.LOG_BOX_HEIGHT
        log_box_width = sconsts.Interface.LOG_BOX_WIDTH

        GameInterface.draw_info_box(stdscr,
                                    info_box_height,
                                    info_box_width,
                                    info_context)
        
        GameInterface.draw_dialog_box(stdscr, info_box_height, dialog_box_dimensions, dialog_context)
        
        GameInterface.draw_dungeon_box(stdscr,
                                       interface_width,
                                       dungeon_box_size,
                                       dungeon_dimensions,
                                       player_location,
                                       enemies,
                                       info_box_height)

        GameInterface.draw_log_box(stdscr,
                                   info_box_height,
                                   dungeon_box_size,
                                   log_box_height,
                                   log_box_width,
                                   log_context,
                                   log_cursor)
        
    def draw_game_over(stdscr, go_text):
        go_height = sconsts.Interface.HEIGHT
        go_width = sconsts.Interface.WIDTH

        GameInterface.draw_box(stdscr, 0, 0, go_height, go_width)

        start_y = go_height // 2 - len(go_text) // 2

        for i, line in enumerate(go_text):
            start_x = (go_width - len(line)) // 2
            stdscr.addstr(start_y + i, start_x, line)

    def draw_info_box(stdscr,
                      inf_box_height,
                      info_box_width,
                      info_box_context):
        GameInterface.draw_box(stdscr, 0, 0, inf_box_height, info_box_width, title="Info")
        GameInterface.draw_text_in_box(stdscr, 0, 0, inf_box_height, info_box_width, info_box_context)


    def draw_dialog_box(stdscr,
                        info_box_height,
                        dialog_box_dimensions,
                        dialog_box_context):
        height, width = dialog_box_dimensions
        left = 0
        top = info_box_height

        GameInterface.draw_box(stdscr, top, left, height, width, title="Dialog")

        #TODO: Add paging with -/+
        for i, line in enumerate(dialog_box_context):
            if i >= height - 2:
                break
            stdscr.addstr(top + 1 + i, left + 1, line)

    def draw_dungeon_box(stdscr,
                         interface_width,
                         dungeon_box_size,
                         dungeon_dimensions,
                         player_location,
                         enemies,
                         info_box_height):
        # Set position aligment to middle of the interface
        d_box_pos = (interface_width // 2) - (dungeon_box_size // 2)
        dungeon_height, dungeon_width = dungeon_dimensions
        player_loc_y, player_loc_x = player_location

        dungeon_grid = [[" " for _ in range(dungeon_width)] for _ in range(dungeon_height)]
        dungeon_grid[player_loc_y][player_loc_x] = "@"

        for enemy in enemies:
            e_pos_y = enemy.position_y
            e_pos_x = enemy.position_x
            dungeon_grid[e_pos_y][e_pos_x] = str(enemy.id)

        GameInterface.draw_box(stdscr,
                               info_box_height,
                               d_box_pos,
                               dungeon_box_size, # Height
                               dungeon_box_size, # Width
                               title="Dungeon")

        # -2 Negating box borders so actual inside area is max undeon size + walls
        GameInterface.draw_dungeon_grid(stdscr,
                                        info_box_height,
                                        d_box_pos,
                                        dungeon_box_size - 2, # 20X20 Dungeon box - 2X2
                                        dungeon_box_size - 2, # 18X18 Wall zone - Part of the grid
                                        dungeon_height,       # 16X16 Dungeon zone
                                        dungeon_width,
                                        dungeon_grid)
        
        
    def draw_log_box(stdscr, info_box_height, dungeon_box_height, log_box_height, width, log_context, log_cursor):
        GameInterface.draw_box(stdscr, info_box_height + dungeon_box_height, 0, log_box_height, width, title="Log")
        
        visible_logs = log_context[log_cursor:log_cursor + log_box_height - 2]

        for i, line in enumerate(visible_logs):
            stdscr.addstr(info_box_height + dungeon_box_height + 1 + i, 2, line)


    def draw_box(stdscr, top, left, height, width, title=""):
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


    def draw_text_in_box(stdscr, top, left, height, width, text):
        """Draw text inside a box, wrapping it to fit width."""
        # Leave 1 character padding on each side
        max_width = width - 2
        lines = text.split("\n")  # preserve explicit newlines
        wrapped_lines = []

        for line in lines:
            wrapped_lines.extend(textwrap.wrap(line, max_width))
    
        for i, line in enumerate(wrapped_lines):
            # Make sure we don't write outside the box height
            if i >= height - 2:
                break
            stdscr.addstr(top + 1 + i, left + 1, line)


    def draw_dungeon_grid(stdscr, top, left, inner_height, inner_width, dungeon_height, dungeon_width, dungeon_grid):
        """
        Draw the dungeon inside the dungeon box, with a wall layer around it.
    
        inner_height, inner_width: the space inside the borders (box_size - 2)
        """
        # Offsets so the dungeon is centered inside the inner area
        y_offset = (inner_height - dungeon_height) // 2
        x_offset = (inner_width - dungeon_width) // 2

        for y in range(inner_height):
            for x in range(inner_width):
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
                    stdscr.addstr(top + 1 + y, left + 1 + x, ch)
                else:
                    # Fill walls in padding layer
                    stdscr.addstr(top + 1 + y, left + 1 + x, "■")