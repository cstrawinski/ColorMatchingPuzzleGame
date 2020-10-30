from operator import itemgetter
from colors import BlockColor
from Block import Block
from BlockType import BlockType
import random


class Board:
    def __init__(self, dimensions, board_position, surface_manager):
        self._width, self._height = dimensions
        self._position = board_position
        self._playable_area = []
        self._surface_manager = surface_manager

    def new(self, level, position):
        self._position = position
        self._width = level['board_width']
        self._height = level['board_height']
        self._playable_area = [[self.random_block() for x in range(self._width)]
                               for y in range(self._height)]
        for block in level['level_data']:
            x, y, typ, color_name = block
            block_surfaces = self._surface_manager.get_block_surfaces(BlockType(typ))
            self._playable_area[y][x] = Block(BlockColor.BLACK,
                                              self._position,
                                              block_surfaces[BlockColor[color_name]],
                                              BlockType(typ))

    def draw(self, dst_surface):
        [[self._playable_area[y][x].draw(x, y, dst_surface) for x in range(self._width)] for y in range(self._height)]

    def click_block(self, pos):
        pos_x, pos_y = pos
        board_pos = (pos_x - self._position[0], pos_y - self._position[1])
        if board_pos[0] < 0 or board_pos[1] < 0:
            return

        clicked_block = (int(board_pos[0] / Block.SIZE[0]),
                         int(board_pos[1] / Block.SIZE[1]))

        if clicked_block[0] >= self._width or clicked_block[1] >= self._height:
            return

        print('Block at [%s, %s] was clicked' % clicked_block)
        return clicked_block

    def get_block_at(self, pos):
        pos_x, pos_y = pos
        return self._playable_area[pos_y][pos_x]

    def get_connected_blocks(self, start_pos, connected_set):
        block_x, block_y = start_pos
        block = self._playable_area[block_y][block_x]
        connected_set.add(start_pos)

        # Check left
        if block_x > 0 and self._playable_area[block_y][block_x - 1].is_equal(block) and not (block_x - 1, block_y) in connected_set:
            self.get_connected_blocks((block_x - 1, block_y), connected_set)
        # Check up
        if block_y > 0 and self._playable_area[block_y - 1][block_x].is_equal(block) and not (block_x, block_y - 1) in connected_set:
            self.get_connected_blocks((block_x, block_y - 1), connected_set)
        # Check right
        if block_x < (self._width - 1) and self._playable_area[block_y][block_x + 1].is_equal(block) and not (block_x + 1, block_y) in connected_set:
            self.get_connected_blocks((block_x + 1, block_y), connected_set)
        # Check down
        if block_y < (self._height - 1) and self._playable_area[block_y + 1][block_x].is_equal(block) and not (block_x, block_y + 1) in connected_set:
            self.get_connected_blocks((block_x, block_y + 1), connected_set)

        return connected_set

    def clear(self, connected_set):
        [self._playable_area[b[1]][b[0]].set_color(BlockColor.BLACK) for b in connected_set]

    def fill_empty_blocks(self, empty_set):
        sorted_by_x = sorted(empty_set, key=itemgetter(0))
        empty_block_list = sorted(sorted_by_x, key=itemgetter(1))
        print(empty_block_list)
        [self._move_blocks_down(block_pos) for block_pos in empty_block_list]

    def random_block(self):
        all_blocks = self._surface_manager.get_block_colors()
        surfaces = self._surface_manager.get_block_surfaces(BlockType.NORMAL)
        color_num = random.randint(0, len(all_blocks) - 1)
        block_color = all_blocks[color_num]
        return Block(block_color, self._position, surfaces[block_color])

    def _copy_from(self, pos):
        pos_x, pos_y = pos
        block = self._playable_area[pos_y][pos_x]
        return Block(block.get_color(), self._position, block.get_image(), block.get_block_type())

    def _move_blocks_down(self, pos):
        pos_x, pos_y = pos
        block_above = self._get_next_fallible_block_pos(pos)
        if pos_y > 0 and block_above is not None:
            self._playable_area[pos_y][pos_x] = self._copy_from(block_above)
            self._move_blocks_down(block_above)
        else:
            self._playable_area[pos_y][pos_x] = self.random_block()

    def _get_next_fallible_block_pos(self, cur_block_pos):
        pos_x, pos_y = cur_block_pos
        pos_y -= 1
        while pos_y >= 0 and not self._playable_area[pos_y][pos_x].should_fall():
            pos_y -= 1

        if pos_y >= 0:
            return pos_x, pos_y

        return None
