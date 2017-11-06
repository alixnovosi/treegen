"""Setup for tree_bot"""

from os import path
from setuptools import setup, find_packages

HERE = path.abspath(path.dirname(__file__))

with open(path.join(HERE, "VERSION"), encoding="utf-8") as f:
    VERSION = f.read().strip()

setup(author="Andrew Michaud",
      author_email="bots+tree@mail.andrewmichaud.com",
      url="https://github.com/andrewmichaud/tree_bot",

      entry_points={"console_scripts": ["tree__bot = tree_bot.__main__:main"]},

      install_requires=["botskeleton>=1.1.0", "Pillow"],

      license="BSD3",

      name="tree_bot",

      packages=find_packages(),

      version=VERSION)
