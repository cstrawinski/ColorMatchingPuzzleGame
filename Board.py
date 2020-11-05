from operator import itemgetter
from AnimationManager import AnimationManager
from Block import Block
from colors import BlockColor
from BlockType import BlockType
from SurfaceManager import SurfaceManager
import random
import pygame


class Board:
    def __init__(self, dimensions: (int, int), board_position: (int, int), surface_manager: SurfaceManager,
                 animation_manager: AnimationManager):
        self._width, self._height = dimensions
        self._position = board_position
        self._playable_area = []
        self._surface_manager = surface_manager

    def new(self, level: {str: object}, position: (int, int)):
        """
        Creates a new board with the level data for the given level
        :param level: Dictionary of level data loaded from file
        :param position: Window x, y coordinates to place upper-left corner of playable area
        :return: None
        """
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

    def draw(self, dst_surface: pygame.Surface):
        [[self._playable_area[y][x].draw(x, y, dst_surface) for x in range(self._width)] for y in range(self._height)]

    def click_block(self, pos: (int, int)) -> (int, int):
        """
        Locates the block clicked at the given pos (in window coordinates)
        :param pos: Tuple with x, y coordinates of window position clicked
        :return: Tuple with x, y coordinates of block clicked
        """
        pos_x, pos_y = pos
        board_pos = (pos_x - self._position[0], pos_y - self._position[1])
        if board_pos[0] < 0 or board_pos[1] < 0:
            return None

        clicked_block = (int(board_pos[0] / Block.SIZE[0]),
                         int(board_pos[1] / Block.SIZE[1]))

        if clicked_block[0] >= self._width or clicked_block[1] >= self._height:
            return None

        print('Block at [%s, %s] was clicked' % clicked_block)
        return clicked_block

    def get_block_at(self, pos: (int, int)) -> Block:
        pos_x, pos_y = pos
        return self._playable_area[pos_y][pos_x]

    def get_connected_blocks(self, start_pos: (int, int), connected_set=None) -> {(int, int)}:
        """
        Find and return all identical blocks that are connected to the block at start_pos.
        :param start_pos: Tuple with x, y coordinate of starting block to search
        :param connected_set: Working set of connected blocks. Do not use when calling this function.
        :return: Set of tuples with x, y coordinates of all matching blocks connected to block at start_pos.
        """
        block_x, block_y = start_pos
        block = self._playable_area[block_y][block_x]
        if connected_set is None:
            connected_set = set()
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

    def clear(self, connected_set: {(int, int)}):
        """
        Set all blocks at locations in connected_set to an empty Block (BlockType.NONE)
        :param connected_set: Set of tuples with x, y coordinates of blocks to clear
        :return: None
        """
        # [self._playable_area[b[1]][b[0]].set_color(BlockColor.BLACK) for b in connected_set]
        for b in connected_set:
            self._playable_area[b[1]][b[0]] = self.empty_block()

    def check_adjacent_blocks(self, cleared_set: {(int, int)}) -> {(int, int, Block)}:
        """
        Checks adjacent blocks to cleared_set and returns additional blocks that should be cleared
        :param cleared_set: {(int: x, int: y)}
        :return: {(int: x, int: y, Block)} - Set of tuples with x, y coordinates and Block that need to be cleared
        and filled in.
        """
        sorted_by_x = sorted(cleared_set, key=itemgetter(0))
        sorted_by_y = sorted(sorted_by_x, key=itemgetter(1))
        adjacent_blocks = set()
        for b in sorted_by_y:
            b_x, b_y = b
            if b_x > 0 and (b_x - 1, b_y) not in cleared_set:
                adjacent_blocks.add((b_x - 1, b_y))
            if b_x < (self._width - 1) and (b_x + 1, b_y) not in cleared_set:
                adjacent_blocks.add((b_x + 1, b_y))
            if b_y > 0 and (b_x, b_y - 1) not in cleared_set:
                adjacent_blocks.add((b_x, b_y - 1))
            if b_y < (self._height - 1) and (b_x, b_y + 1) not in cleared_set:
                adjacent_blocks.add((b_x, b_y + 1))

        extra = set()
        # Now loop over adjacent blocks, damaging the blocks that need a good smacking
        for b in adjacent_blocks:
            if self._playable_area[b_y][b_x].is_affected_by_adjacent_clear():
                if self._playable_area[b_y][b_x].damage():
                    # Should clear this block, but we also need to check for empty blocks below it now otherwise
                    # they do not fill in
                    b_x, b_y = b
                    extra.add((b_x, b_y, self._playable_area[b_y][b_x]))
                    b_y += 1
                    while b_y < self._height and self._playable_area[b_y][b_x].get_block_type() == BlockType.NONE:
                        extra.add((b_x, b_y, self._playable_area[b_y][b_x]))
                        b_y += 1

        return extra

    def fill_empty_blocks(self, empty_set: {(int, int)}):
        """
        Collapses blocks above empty_set, filling it in. New blocks will be created as needed.
        :param empty_set: Set of tuples with x, y coordinates of blocks to fill in.
        :return: None
        """
        sorted_by_x = sorted(empty_set, key=itemgetter(0))
        empty_block_list = sorted(sorted_by_x, key=itemgetter(1))
        print(empty_block_list)
        [self._move_blocks_down(block_pos) for block_pos in empty_block_list]

    def random_block(self) -> Block:
        """
        Creates a random colored block
        :return: The new block
        """
        all_blocks = self._surface_manager.get_block_colors()
        surfaces = self._surface_manager.get_block_surfaces(BlockType.NORMAL)
        color_num = random.randint(0, len(all_blocks) - 1)
        block_color = all_blocks[color_num]
        return Block(block_color, self._position, surfaces[block_color])

    def empty_block(self):
        """
        Creates an empty block
        :return: An empty Block
        """
        surfaces = self._surface_manager.get_block_surfaces(BlockType.NONE)
        return Block(BlockColor.BLACK, self._position, surfaces[BlockColor.BLACK], BlockType.NONE)

    def _copy_from(self, pos: (int, int)):
        pos_x, pos_y = pos
        block = self._playable_area[pos_y][pos_x]
        return Block(block.get_color(), self._position, block.get_image(), block.get_block_type())

    def _move_blocks_down(self, pos: (int, int)):
        pos_x, pos_y = pos
        block_above = self._get_next_fallible_block_pos(pos)
        if pos_y > 0 and block_above is not None:
            self._playable_area[pos_y][pos_x] = self._copy_from(block_above)
            self._move_blocks_down(block_above)
        elif pos_y == 0 or not self._playable_area[pos_y - 1][pos_x].stops_blocks_above():
            self._playable_area[pos_y][pos_x] = self.random_block()
        else:
            self._playable_area[pos_y][pos_x] = self.empty_block()

    def _get_next_fallible_block_pos(self, cur_block_pos: (int, int)) -> (int, int):
        """
        Locates the x, y coordinates of the next block above cur_block_pos that can fall down. Returns None
        if none found.
        :param cur_block_pos: Tuple with x, y coordinates of starting block.
        :return: Tuple with x, y coordinates of next block above that can fall. None, if no blocks above should fall.
        """
        pos_x, pos_y = cur_block_pos
        pos_y -= 1

        while pos_y >= 0 and not self._playable_area[pos_y][pos_x].should_fall():
            # If this block keeps blocks above from falling, stop here
            if self._playable_area[pos_y][pos_x].stops_blocks_above():
                return None

            pos_y -= 1

        if pos_y >= 0:
            return pos_x, pos_y

        return None
