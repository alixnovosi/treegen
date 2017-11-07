"""Draw"""

import logging
from datetime import datetime

import treegen

LOG = logging.getLogger("root")

if __name__ == "__main__":
    IMAGE_PATH = path.join(HERE, f"test-{datetime.now()}.png")
    tree_info = treegen.TreeInfo(colors=False, extra_branching=False, IMAGE_PATH=IMAGE_PATH)
    treegen.draw(tree_info)
