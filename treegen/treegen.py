"""Draw trees."""

import enum
import math
import logging
import random
from datetime import datetime
from os import path

from PIL import Image, ImageDraw

from constants import *

LOG = logging.getLogger("root")

class Seasons(enum.Enum):
    """Seasons we support."""
    WINTER = 0
    FALL = 100
    SUMMER = 200
    SPRING = 300


class TreeInfo:
    """Info on tree, to aid recursive drawing."""
    def __init__(self, colors=True, angle_rand=True, branch_rand=True, extra_branching=True,
                 season=None, mixed_fall=False, inverted=False, image_path="test.png"):
        self.x = WIDTH // 2
        self.y = HEIGHT
        self.angle = 0
        self.depth = 0

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

        # Pick a season at random if none was chosen.
        if season is None:
            self.season = random.choice(list(Seasons))
        else:
            self.season = season

        # Have some more branching near the end. Force disable for winter.
        self.extra_branching = extra_branching and not self.season is Seasons.WINTER

        # Mix up colors in fall trees.
        self.mixed_fall = mixed_fall
        if not mixed_fall:
            self.fall_color = random.choice(FALL_LEAVES)

        # Create image and draw object.
        self.image = Image.new("RGBA", (WIDTH, HEIGHT), BG)
        self.imagedraw = ImageDraw.Draw(self.image)

    def draw(self):
        """Draw a tree with the magic of recursion."""
        self.draw_rec()

        self.image.save(self.image_path)

    def pick_color(self):
        """Pick color for current tree bit based on tree_info, depth."""
        if self.colors:
            if self.depth == DEPTH-1:

                if self.season == Seasons.SUMMER:
                    return LEAF_GREEN
                elif self.season == Seasons.FALL:
                    if not self.mixed_fall:
                        return self.fall_color
                    else:
                        return random.choice(FALL_LEAVES)
                elif self.season == Seasons.SPRING:
                    return LEAF_PINK
                elif self.season == Seasons.WINTER:
                    return TREE_BROWN
                else:
                    return LEAF_GREEN

            else:
                return TREE_BROWN

        elif not self.inverted:
            return BLACK
        else:
            return WHITE

    def pick_branch_size(self):
        """Pick new branch length based on depth."""
        if self.branch_rand:
            return (SIZE * ((2/3) ** self.depth)) * (random.choice(BRANCH_LEN_MODIFIERS) / 10)

        return SIZE * ((2/3) ** self.depth)

    def pick_branch_width(self):
        """Pick new branch width based on depth."""
        return int((BASE_WIDTH * (0.69 ** self.depth)) // 1)

    def get_new_coords(self, size):
        """Get new x, y based on branch we want to draw."""
        new_x = self.x - (size * math.sin(self.angle))
        new_y = self.y - (size * math.cos(self.angle))
        return (new_x, new_y)

    def get_ang(self):
        """Get random angle, for left or right side."""
        if self.angle_rand:
            return math.radians(BASE_ANG + random.choice(ANGLE_MODIFIERS))

        return math.radians(BASE_ANG)

    def get_shifts(self, ang, width):
        """Get shifts vertically and horizontally that we need to make line joins work (ish)."""
        h_shift = math.cos(ang) * ((width - width // 2) // 2)
        v_shift = math.sin(ang) * ((width - width // 2) // 2)
        return (h_shift, v_shift)

    def draw_rec(self):
        """Recursively draw a tree."""

        # Increase depth.
        self.depth += 1

        # Stop, eventually.
        if self.depth == DEPTH:
            self.depth -= 1
            return

        # Calculate colors and branch dimensions.
        fill = self.pick_color()
        size = self.pick_branch_size()
        width = self.pick_branch_width()

        old_x = self.x
        old_y = self.y

        (new_x, new_y) = self.get_new_coords(size)

        # Draw root of this tree section.
        self.imagedraw.line([(self.x, self.y), (new_x, new_y)], fill=fill, width=width)

        # Move x and y so recursion starts drawing at the correct place.
        self.y = new_y
        self.x = new_x

        ### LEFT SIDE ####
        left_ang = self.get_ang()
        self.angle += -left_ang

        # Handle line joins being bad by shifting over based on width and angle.
        (h_shift, v_shift) = self.get_shifts(left_ang, width)
        self.x += h_shift
        self.y += v_shift

        self.draw_rec()

        # Restore angle we started with and x, y we started with.
        self.angle += left_ang
        self.x -= h_shift
        self.y -= v_shift

        # Branch more near the end.
        if self.extra_branching:
            if self.depth >= random.choice(range(4, DEPTH)):
                self.angle += -left_ang * 3
                self.draw_rec()
                self.angle += left_ang * 3

        ### MIDDLE ####
        self.draw_rec()

        ### RIGHT SIDE ###
        right_ang = self.get_ang()
        self.angle += right_ang

        # Handle line joins being bad by shifting over based on width and angle.
        (h_shift, v_shift) = self.get_shifts(right_ang, width)
        self.x -= h_shift
        self.y += v_shift

        self.draw_rec()

        # Restore angle we started with and x, y we started with.
        self.angle += -right_ang
        self.x += h_shift
        self.y -= v_shift

        # Branch more near the end.
        if self.extra_branching:
            if self.depth >= random.choice(range(4, DEPTH)):
                self.angle += right_ang * 3
                self.draw_rec()
                self.angle += -right_ang * 3

        # Reset x, y, and depth before finishing this recursive step.
        self.y = old_y
        self.x = old_x
        self.depth -= 1
