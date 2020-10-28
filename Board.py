from operator import itemgetter
from colors import *
from Block import Block
from BlockType import BlockType
import os
import pygame
import random


class Board:
    def __init__(self, width, height, board_position):
        self._width = width
        self._height = height
        self._position = board_position
        self._playable_area = []
        self._block_colors = [RED, GREEN, BLUE, PURPLE]
        self._block_images = pygame.image.load(os.path.join("resources", "blocks.png")).convert_alpha()
        self._block_surfaces = {c: pygame.Surface(Block.SIZE, 0, 32) for c in self._block_colors}
        [self._block_surfaces[c].blit(self._block_images, (0, 0), area=pygame.Rect((i * Block.SIZE[0], 0), Block.SIZE)) for i, c in enumerate(self._block_colors)]
        self._block_surfaces[BlockType.WALL] = pygame.Surface(Block.SIZE, 0, 32)
        self._block_surfaces[BlockType.WALL].blit(self._block_images, (0, 0), area=pygame.Rect((len(self._block_colors) * Block.SIZE[0], 0), Block.SIZE))

    def new(self):
        self._playable_area = [[self.random_block() for x in range(self._width)]
                               for y in range(self._height)]
        # Insert a random wall piece
        wall_x = random.randint(0, self._width - 1)
        wall_y = random.randint(0, self._height - 1)
        self._playable_area[wall_y][wall_x] = Block(BLACK, self._position, self._block_surfaces[BlockType.WALL], BlockType.WALL)

    def draw(self, dst_surface):
        [[self._playable_area[y][x].draw(x, y, dst_surface) for x in range(self._width)] for y in range(self._height)]

    def click_block(self, pos):
        board_pos = (pos[0] - self._position[0], pos[1] - self._position[1])
        if board_pos[0] < 0 or board_pos[1] < 0:
            return

        clicked_block = (int(board_pos[0] / Block.SIZE[0]),
                         int(board_pos[1] / Block.SIZE[1]))

        if clicked_block[0] >= self._width or clicked_block[1] >= self._height:
            return

        print('Block at [%s, %s] was clicked' % (clicked_block[0], clicked_block[1]))
        return clicked_block

    def get_connected_blocks(self, start_pos, connected_set):
        color = self._playable_area[start_pos[1]][start_pos[0]].get_color()
        connected_set.add(start_pos)

        # Check left
        if start_pos[0] > 0 and self._playable_area[start_pos[1]][start_pos[0] - 1].get_color() == color and not (start_pos[0] - 1, start_pos[1]) in connected_set:
            self.get_connected_blocks((start_pos[0] - 1, start_pos[1]), connected_set)
        # Check up
        if start_pos[1] > 0 and self._playable_area[start_pos[1] - 1][start_pos[0]].get_color() == color and not (start_pos[0], start_pos[1] - 1) in connected_set:
            self.get_connected_blocks((start_pos[0], start_pos[1] - 1), connected_set)
        # Check right
        if start_pos[0] < (self._width - 1) and self._playable_area[start_pos[1]][start_pos[0] + 1].get_color() == color and not (start_pos[0] + 1, start_pos[1]) in connected_set:
            self.get_connected_blocks((start_pos[0] + 1, start_pos[1]), connected_set)
        # Check down
        if start_pos[1] < (self._height - 1) and self._playable_area[start_pos[1] + 1][start_pos[0]].get_color() == color and not (start_pos[0], start_pos[1] + 1) in connected_set:
            self.get_connected_blocks((start_pos[0], start_pos[1] + 1), connected_set)

        return connected_set;

    def clear(self, connected_set):
        [self._playable_area[b[1]][b[0]].set_color(BLACK) for b in connected_set]

    def fill_empty_blocks(self, empty_set):
        sorted_by_x = sorted(empty_set, key=itemgetter(0))
        empty_block_list = sorted(sorted_by_x, key=itemgetter(1))
        print(empty_block_list)
        [self._move_blocks_down(block_pos) for block_pos in empty_block_list]

    def random_block(self):
        color_num = random.randint(0, len(self._block_colors) - 1)
        block_color = self._block_colors[color_num]
        return Block(block_color, self._position, self._block_surfaces[block_color])

    def _copy_from(self, pos):
        block = self._playable_area[pos[1]][pos[0]]
        return Block(block.get_color(), self._position, block.get_image())

    def _move_blocks_down(self, pos):
        block_above = self._get_next_fallible_block_pos(pos)
        if pos[1] > 0 and block_above is not None:
            self._playable_area[pos[1]][pos[0]] = self._copy_from(block_above)
            self._move_blocks_down(block_above)
        else:
            self._playable_area[pos[1]][pos[0]] = self.random_block()

    def _get_next_fallible_block_pos(self, cur_block_pos):
        pos = (cur_block_pos[0], cur_block_pos[1] - 1)
        while pos[1] >= 0 and self._playable_area[pos[1]][pos[0]].get_block_type() == BlockType.WALL:
            pos = (pos[0], pos[1] - 1)

        if pos[1] >= 0:
            return pos

        return None
