"""Draw"""

import math
from os import path
from PIL import Image, ImageDraw

DEPTH = 5

HERE = path.abspath(path.dirname(__file__))
IMAGE_PATH = path.join(HERE, "test.png")
WIDTH = 1000
HEIGHT = 1600
BLUE = (50, 20, 200)

ANG = math.radians(30)

SIZE = HEIGHT // 3


class ImageState:
    """State of image, to aid recursive drawing."""
    def __init__(self):
        self.x = WIDTH // 2
        self.y = HEIGHT
        self.angle = 0

        if not path.isfile(IMAGE_PATH):
            with open(IMAGE_PATH, "a") as f:
                f.close()

        self.im = Image.new("RGB", (WIDTH, HEIGHT), BLUE)

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

    size = SIZE / 2**(depth)
    print(f"size={size}")
    print(f"drawing 'trunk'")

    old_x = image_state.x
    old_y = image_state.y

    new_x = image_state.x - (size * math.sin(image_state.angle))
    new_y = image_state.y - (size * math.cos(image_state.angle))
    image_state.draw.line([(image_state.x, image_state.y), (new_x, new_y)],
                          fill=(0, 0, 0), width=2)
    image_state.y = new_y
    image_state.x = new_x

    print(f"rotating left, doing left branch")
    image_state.angle -= math.radians(30)
    draw(image_state, depth+1)

    image_state.angle += math.radians(30)

    print(f"rotating right, doing right branch")
    image_state.angle += math.radians(30)
    draw(image_state, depth+1)

    # reset coords
    image_state.y = old_y
    image_state.x = old_x

    image_state.angle -= math.radians(30)

    print("done here")

if __name__ == "__main__":
    main()
