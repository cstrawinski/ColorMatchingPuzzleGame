from enum import Enum


class BlockType(Enum):
    NONE = 0
    EMPTY = 1
    NORMAL = 2  # Standard colored blocks
    WALL = 3
