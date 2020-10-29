from enum import Enum


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (127, 127, 127)


class BlockColor(Enum):
    WHITE = WHITE
    BLACK = BLACK
    GRAY = GRAY
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    PURPLE = (255, 0, 255)
    YELLOW = (255, 255, 0)