"""Constants for tree generation."""

from os import path

DEPTH = 10

HERE = path.abspath(path.dirname(__file__))

WIDTH = 1920
HEIGHT = 1080

# Colors.
SKY_BLUE = (157, 175, 247, 254)
SKY_WHITE = (255, 255, 255, 254)

# Leaf colors.
LEAF_GREEN = (52, 186, 106, 254)

LEAF_YELLOW = (207, 162, 65)
LEAF_RED = (204, 69, 38, 254)
LEAF_BROWN = (181, 108, 36, 254)

LEAF_PINK = (255, 183, 197, 254)

LEAF_WHITE = (255, 255, 255, 254)

FALL_LEAVES = [LEAF_YELLOW, LEAF_RED, LEAF_BROWN]

# Other colors.
TREE_BROWN = (98, 90, 21, 254)

BLACK = (0, 0, 0, 254)
WHITE = (255, 255, 255, 254)

# Tree factors.
BASE_ANG = 30
BASE_WIDTH = 20

SIZE = HEIGHT // 3

# Randomization factors.
ANGLE_MODIFIERS = range(-30, 31, 1)
BRANCH_LEN_MODIFIERS = range(4, 11)
