"""Draw trees."""

import math
import logging
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
BLUE = (157, 175, 247, 254)
GREEN = (52, 186, 106, 254)
BROWN = (98, 90, 21, 254)
BLACK = (0, 0, 0, 254)
WHITE = (255, 255, 255, 254)

BASE_ANG = 30
BASE_WIDTH = 20

SIZE = HEIGHT // 3

LOG = logging.getLogger("root")


class TreeInfo:
    """Info on tree, to aid recursive drawing."""
    def __init__(self, colors=True, angle_rand=True, branch_rand=True, extra_branching=True):
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

        # Have some more branching near the end.
        self.extra_branching = extra_branching

        self.im = Image.new("RGBA", (WIDTH, HEIGHT), BG)

        self.draw = ImageDraw.Draw(self.im)

def draw(tree_info):
    """Draw a tree with the magic of recursion."""
    draw_rec(tree_info, 0)

    tree_info.im.save(IMAGE_PATH)

def draw_rec(tree_info, depth):
    """Recursively draw a tree."""
    LOG.debug(f"depth={depth}")
    if depth == DEPTH:
        LOG.debug(f"depth equal to {DEPTH}, returning")
        return

    # Draw leaves at the end.
    if tree_info.colors:
        if depth == DEPTH-1:
            LOG.debug(f"leaves")
            fill = GREEN
        else:
            LOG.debug(f"branches")
            fill = BROWN
    else:
        fill = BLACK

    # Stretch or shrink branches to add randomness.
    if tree_info.branch_rand:
        size = (SIZE * ((2/3) ** depth)) * (random.choice(range(4, 11)) / 10)
    else:
        size = SIZE * ((2/3) ** depth)

    # Shrink branches as we go on.
    width = BASE_WIDTH // (2 ** depth)

    # Start with trunk, or what we think is the trunk.
    LOG.debug(f"size={size}")
    LOG.debug(f"drawing 'trunk'")

    old_x = tree_info.x
    old_y = tree_info.y

    # Actual trunk drawing.
    new_x = tree_info.x - (size * math.sin(tree_info.angle))
    new_y = tree_info.y - (size * math.cos(tree_info.angle))
    tree_info.draw.line([(tree_info.x, tree_info.y), (new_x, new_y)],
                          fill=fill, width=width)

    # Move x and y for recursion.
    tree_info.y = new_y
    tree_info.x = new_x

    # Left.
    LOG.debug(f"rotating left, doing left branch")
    if tree_info.angle_rand:
        left_ang = math.radians(BASE_ANG + random.choice(range(-20, 21, 1)))
    else:
        left_ang = math.radians(BASE_ANG)

    LOG.debug(f"left ang {left_ang}")
    tree_info.angle += -left_ang
    draw_rec(tree_info, depth+1)

    tree_info.angle += left_ang

    # Branch more near the end.
    if tree_info.extra_branching:
        if depth >= random.choice(range(4, DEPTH)):
            tree_info.angle += -left_ang * 3
            draw_rec(tree_info, depth+1)

            tree_info.angle += left_ang * 3

    LOG.debug(f"center branch")
    draw_rec(tree_info, depth+1)

    # Right
    LOG.debug(f"rotating right, doing right branch")
    if tree_info.angle_rand:
        right_ang = math.radians(BASE_ANG + random.choice(range(-20, 21, 1)))
    else:
        right_ang = math.radians(BASE_ANG)

    LOG.debug(f"right ang {right_ang}")
    tree_info.angle += right_ang
    draw_rec(tree_info, depth+1)

    tree_info.angle += -right_ang

    # Branch more near the end.
    if tree_info.extra_branching:
        if depth >= random.choice(range(4, DEPTH)):
            tree_info.angle += right_ang * 3
            draw_rec(tree_info, depth+1)

            tree_info.angle += -right_ang * 3

    # Reset before finishing this recursive step.
    tree_info.y = old_y
    tree_info.x = old_x

    LOG.debug("done here")
