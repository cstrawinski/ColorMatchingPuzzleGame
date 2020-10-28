import pygame
from BlockType import BlockType


class Block:
    SIZE = (32, 32)

    def __init__(self, color, offset, image, block_type=None):
        self._color = color
        self._offset = offset
        self._image = image
        self._block_type = block_type
        if block_type is None:
            self._block_type = BlockType.NORMAL

    def draw(self, x, y, dst_surface):
        dst_surface.blit(self._image, (x * self.SIZE[0] + self._offset[0], y * self.SIZE[1] + self._offset[1]))

    def set_color(self, color):
        self._color = color

    def get_color(self):
        return self._color

    def get_image(self):
        return self._image

    def get_block_type(self):
        return self._block_type

    def set_block_type(self, block_type):
        self._block_type = block_type
