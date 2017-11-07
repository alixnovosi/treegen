"""Draw"""

import logging

import tree_gen

LOG = logging.getLogger("root")

if __name__ == "__main__":
    tree_info = tree_gen.TreeInfo()
    tree_gen.draw(tree_info)
