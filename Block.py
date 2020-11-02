from BlockType import BlockType


class Block:
    SIZE = (32, 32)

    def __init__(self, color, offset, image, block_type=None, life=1):
        self._color = color
        self._block_type = block_type
        self._life = life
        self._offset = offset
        self._image = image
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

    def is_equal(self, other):
        return self._color == other.get_color() and\
               self._block_type == other.get_block_type()

    def should_fall(self):
        return self._block_type == BlockType.NORMAL

    def stops_blocks_above(self):
        return self._block_type == BlockType.CRATE or \
               self._block_type == BlockType.NONE

    def is_affected_by_adjacent_clear(self):
        return self._block_type == BlockType.CRATE

    def damage(self):
        self._life -= 1
        return self._life <= 0
