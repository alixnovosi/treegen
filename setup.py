"""Setup for treebot"""

from os import path
from setuptools import setup, find_packages

HERE = path.abspath(path.dirname(__file__))

with open(path.join(HERE, "VERSION"), encoding="utf-8") as f:
    VERSION = f.read().strip()

setup(author="Andrew Michaud",
      author_email="dev@mail.andrewmichaud.com",
      url="https://github.com/andrewmichaud/treegen",

      entry_points={"console_scripts": ["treegen = treegen.__main__:main"]},

      install_requires=["botskeleton>=1.1.0", "Pillow"],

      license="BSD3",

      name="treegen",

      packages=find_packages(),

      version=VERSION)
