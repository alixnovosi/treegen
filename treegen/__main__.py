"""Draw"""

import logging
from datetime import datetime
from os import path

import treegen

LOG = logging.getLogger("root")

if __name__ == "__main__":
    HERE = path.abspath(path.dirname(__file__))
    IMAGE_PATH = path.join(HERE, f"test.png")
    tree_info = treegen.TreeInfo(image_path=IMAGE_PATH)
    tree_info.draw()
