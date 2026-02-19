import pygame as pg

def flood_fill(surface, x, y, new_color):
    # 1. Get the screen size
    width, height = surface.get_size()

    # 2. Check if the starting pixel is outside the screen
    if x < 0 or x >= width or y < 0 or y >= height:
        return

    target_color = surface.get_at((x, y))
    if target_color == new_color:
        return

    # To avoid immediate crash, we use a stack-based fill 
    # (Recursion is very risky with screen-sized boundaries)
    stack = [(x, y)]
    while stack:
        curr_x, curr_y = stack.pop()

        # Boundary check for each pixel
        if 0 <= curr_x < width and 0 <= curr_y < height:
            if surface.get_at((curr_x, curr_y)) == target_color:
                surface.set_at((curr_x, curr_y), new_color)
                stack.append((curr_x + 1, curr_y))
                stack.append((curr_x - 1, curr_y))
                stack.append((curr_x, curr_y + 1))
                stack.append((curr_x, curr_y - 1))
