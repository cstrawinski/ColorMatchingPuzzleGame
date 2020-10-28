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
        width, height = self.SIZE
        offset_x, offset_y = self._offset
        dst_surface.blit(self._image, (x * width + offset_x, y * height + offset_y))

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
