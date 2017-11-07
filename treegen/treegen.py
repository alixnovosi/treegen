"""Draw trees."""

import enum
import math
import logging
import random
from datetime import datetime
from os import path

from PIL import Image, ImageDraw

DEPTH = 10

HERE = path.abspath(path.dirname(__file__))

now = datetime.now()

WIDTH = 1600
HEIGHT = 900

# Colors.
SKY_BLUE = (157, 175, 247, 254)
SKY_WHITE = (255, 255, 255, 254)

# Leaf colors.
LEAF_GREEN = (52, 186, 106, 254)

LEAF_YELLOW = (244, 244, 122, 254)
LEAF_RED = (204, 69, 38, 254)
LEAF_BROWN = (181, 108, 36, 254)

LEAF_WHITE = (255, 255, 255, 254)

FALL_LEAVES = [LEAF_YELLOW, LEAF_RED, LEAF_BROWN]

TREE_BROWN = (98, 90, 21, 254)

BLACK = (0, 0, 0, 254)
WHITE = (255, 255, 255, 254)

BASE_ANG = 30
BASE_WIDTH = 20

SIZE = HEIGHT // 3

LOG = logging.getLogger("root")

class Seasons(enum.Enum):
    """Seasons we support."""
    WINTER = 0
    FALL = 100
    SUMMER = 200


class TreeInfo:
    """Info on tree, to aid recursive drawing."""
    def __init__(self, colors=True, angle_rand=True, branch_rand=True, extra_branching=True,
                 season=None, mixed_fall=False, inverted=False, image_path="test.png"):
        self.x = WIDTH // 2
        self.y = HEIGHT
        self.angle = 0

        self.image_path = image_path
        if not path.isfile(image_path):
            with open(image_path, "a") as f:
                f.close()

        # Use colors or just use black and white.
        self.colors = colors
        self.inverted = inverted
        if colors:
            BG = SKY_BLUE
        elif self.inverted:
            BG = BLACK
        else:
            BG = SKY_WHITE

        # Randomize angles left and right, so they're not just BASE_ANGLE.
        self.angle_rand = angle_rand

        # Randomize branch lengths so they're not all the same size.
        self.branch_rand = branch_rand

        # Have some more branching near the end.
        self.extra_branching = extra_branching

        # Pick a season at random if none was chosen.
        if season is None:
            self.season = random.choice(list(Seasons))
        else:
            self.season = season

        # Mix up colors in fall trees.
        self.mixed_fall = mixed_fall
        if not mixed_fall:
            self.fall_color = random.choice(FALL_LEAVES)

        # Create image and draw object.
        self.im = Image.new("RGBA", (WIDTH, HEIGHT), BG)
        self.draw = ImageDraw.Draw(self.im)

def draw(tree_info):
    """Draw a tree with the magic of recursion."""
    draw_rec(tree_info, 0)

    tree_info.im.save(tree_info.image_path)

def draw_rec(tree_info, depth):
    """Recursively draw a tree."""
    #LOG.debug(f"depth={depth}")
    if depth == DEPTH:
        #LOG.debug(f"depth equal to {DEPTH}, returning")
        return

    # Draw leaves at the end.
    if tree_info.colors:
        if depth == DEPTH-1:
            #LOG.debug(f"leaves")

            if tree_info.season == Seasons.SUMMER:
                fill = LEAF_GREEN
            elif tree_info.season == Seasons.FALL:
                if not tree_info.mixed_fall:
                    fill = tree_info.fall_color
                else:
                    fill = random.choice(FALL_LEAVES)
            elif tree_info.season == Seasons.WINTER:
                fill = LEAF_WHITE
            else:
                fill = LEAF_GREEN

        else:
            #LOG.debug(f"branches")
            fill = TREE_BROWN
    elif not tree_info.inverted:
        fill = BLACK
    else:
        fill = WHITE

    # Stretch or shrink branches to add randomness.
    if tree_info.branch_rand:
        size = (SIZE * ((2/3) ** depth)) * (random.choice(range(4, 11)) / 10)
    else:
        size = SIZE * ((2/3) ** depth)

    # Shrink branches as we go on.
    width = BASE_WIDTH // (2 ** depth)

    # Start with trunk, or what we think is the trunk.
    #LOG.debug(f"size={size}")
    #LOG.debug(f"drawing 'trunk'")

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
    #LOG.debug(f"rotating left, doing left branch")
    if tree_info.angle_rand:
        left_ang = math.radians(BASE_ANG + random.choice(range(-20, 21, 1)))
    else:
        left_ang = math.radians(BASE_ANG)

    # Handle line joins being bad by shifting over based on width.
    if width > 1:
        h_shift = math.cos(left_ang) * ((width - width // 2) // 3)
        v_shift = width // 2

        tree_info.x += h_shift

        # Also shift height.
        tree_info.y += v_shift

    #LOG.debug(f"left ang {left_ang}")
    tree_info.angle += -left_ang
    draw_rec(tree_info, depth+1)

    tree_info.angle += left_ang

    if width > 1:
        tree_info.x -= h_shift
        tree_info.y -= v_shift

    # Branch more near the end.
    if tree_info.extra_branching:
        if depth >= random.choice(range(4, DEPTH)):
            tree_info.angle += -left_ang * 3
            draw_rec(tree_info, depth+1)

            tree_info.angle += left_ang * 3

    #LOG.debug(f"center branch")
    draw_rec(tree_info, depth+1)

    # Right
    #LOG.debug(f"rotating right, doing right branch")
    if tree_info.angle_rand:
        right_ang = math.radians(BASE_ANG + random.choice(range(-20, 21, 1)))
    else:
        right_ang = math.radians(BASE_ANG)

    # Handle line joins being bad by shifting over based on width.
    if width > 1:
        h_shift = math.cos(right_ang) * ((width - width // 2) // 3)
        v_shift = width // 2

        tree_info.x -= h_shift

        # Also shift height.
        tree_info.y += v_shift

    #LOG.debug(f"right ang {right_ang}")
    tree_info.angle += right_ang
    draw_rec(tree_info, depth+1)

    tree_info.angle += -right_ang

    if width > 1:
        tree_info.x += h_shift
        tree_info.y -= v_shift

    # Branch more near the end.
    if tree_info.extra_branching:
        if depth >= random.choice(range(4, DEPTH)):
            tree_info.angle += right_ang * 3
            draw_rec(tree_info, depth+1)

            tree_info.angle += -right_ang * 3

    # Reset before finishing this recursive step.
    tree_info.y = old_y
    tree_info.x = old_x

    #LOG.debug("done here")
