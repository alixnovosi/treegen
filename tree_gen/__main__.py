"""Draw"""

import math
import random
from datetime import datetime
from os import path
from PIL import Image, ImageDraw

DEPTH = 10

HERE = path.abspath(path.dirname(__file__))
now = datetime.now()
IMAGE_PATH = path.join(HERE, f"test-{now}.png")
WIDTH = 1600
HEIGHT = 900
BLUE = (157, 175, 247)

BASE_ANG = 30
BASE_WIDTH = 10

SIZE = HEIGHT // 3


class ImageState:
    """State of image, to aid recursive drawing."""
    def __init__(self, colors=True, angle_rand=True, branch_rand=True, fork_inc=True):
        self.x = WIDTH // 2
        self.y = HEIGHT
        self.angle = 0

        if not path.isfile(IMAGE_PATH):
            with open(IMAGE_PATH, "a") as f:
                f.close()

        # Use colors or just use black and white.
        self.colors = colors
        if colors:
            BG = BLUE
        else:
            BG=(255, 255, 255)

        # Randomize angles left and right, so they're not just BASE_ANGLE.
        self.angle_rand = angle_rand

        # Randomize branch lengths so they're not all the same size.
        self.branch_rand = branch_rand

        self.im = Image.new("RGB", (WIDTH, HEIGHT), BG)

        self.draw = ImageDraw.Draw(self.im)

def main():
    """main"""
    draw_help()

def draw_help():
    """start the recursion"""

    image_state = ImageState()

    draw(image_state, 0)

    image_state.im.save(IMAGE_PATH)

def draw(image_state, depth):
    """recursively draw"""
    print(f"depth={depth}")
    if depth == DEPTH:
        print(f"depth equal to {DEPTH}, returning")
        return

    # Draw leaves at the end.
    if image_state.colors:
        if depth == DEPTH-1:
            print(f"leaves")
            fill = (52, 186, 106)
        else:
            print(f"branches")
            fill = (98, 90, 21)
    else:
        fill = (0, 0, 0)

    if image_state.branch_rand:
        size = (SIZE * ((2/3) ** depth)) * (random.choice(range(4, 11)) / 10)
    else:
        size = SIZE * ((2/3) ** depth)

    width = BASE_WIDTH // (2 ** depth)
    print(f"size={size}")
    print(f"drawing 'trunk'")

    old_x = image_state.x
    old_y = image_state.y

    new_x = image_state.x - (size * math.sin(image_state.angle))
    new_y = image_state.y - (size * math.cos(image_state.angle))
    image_state.draw.line([(image_state.x, image_state.y), (new_x, new_y)],
                          fill=fill, width=width)
    image_state.y = new_y
    image_state.x = new_x

    print(f"rotating left, doing left branch")
    if image_state.angle_rand:
        left_ang = math.radians(BASE_ANG + random.choice(range(-20, 21, 1)))
    else:
        left_ang = math.radians(BASE_ANG)

    print(f"left ang {left_ang}")
    image_state.angle += -left_ang
    draw(image_state, depth+1)

    image_state.angle += left_ang

    print(f"center branch")
    draw(image_state, depth+1)

    print(f"rotating right, doing right branch")
    if image_state.angle_rand:
        right_ang = math.radians(BASE_ANG + random.choice(range(-20, 21, 1)))
    else:
        right_ang = math.radians(BASE_ANG)

    print(f"right ang {right_ang}")
    image_state.angle += right_ang
    draw(image_state, depth+1)

    # reset coords
    image_state.y = old_y
    image_state.x = old_x

    image_state.angle += -right_ang

    print("done here")

if __name__ == "__main__":
    main()
