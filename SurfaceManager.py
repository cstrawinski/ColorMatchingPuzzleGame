import pygame
from Block import Block
from BlockType import BlockType
from colors import BlockColor


class SurfaceManager:
    def __init__(self):
        self._block_surfaces = {t: [] for t in BlockType}
        self._block_colors = [BlockColor.RED, BlockColor.GREEN, BlockColor.BLUE, BlockColor.PURPLE]

    def load_blocks(self, filename):
        block_images = pygame.image.load(filename).convert_alpha()
        self._block_surfaces[BlockType.NORMAL] = {c: pygame.Surface(Block.SIZE, 0, 32) for c in self._block_colors}
        self._block_surfaces[BlockType.WALL] = {BlockColor.BLACK: pygame.Surface(Block.SIZE, 0, 32)}

        block_width, block_height = Block.SIZE
        [s[1].blit(block_images, (0, 0), area=pygame.Rect((i * block_width, 0), Block.SIZE)) for i, s in enumerate(self._block_surfaces[BlockType.NORMAL].items())]

        wall_img_idx = len(self._block_colors)
        wall_surface = self._block_surfaces[BlockType.WALL][BlockColor.BLACK]
        wall_surface.blit(block_images, (0, 0), area=pygame.Rect((wall_img_idx * block_width, 0), Block.SIZE))

    def get_block_surfaces(self, block_type):
        return self._block_surfaces[block_type]

    def get_block_colors(self):
        return self._block_colors
