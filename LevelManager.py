from Block import Block
from BlockType import BlockType
from colors import BlockColor
import json


class LevelManager:
    def __init__(self, surface_manager):
        self.level_data = []
        self._surface_manager = surface_manager

    def save(self):
        with open('leveldata.json', 'w') as f:
            json.dump(self.level_data, f)

    def load(self):
        with open('leveldata.json', 'r') as f:
            self.level_data = json.load(f)

    def get_goals(self, level: int) -> {(BlockType, BlockColor): (int, Block)}:
        """
        Retrieves the goals for the given level
        :param level:
        :return: Dictionary of tuples of count, Block representing each type of block and number needed to clear.
        Key is tuple of BlockType, BlockColor
        """
        goal_data = self.level_data[level]['goal']
        goals = {}
        for c, typ, color in goal_data:
            block_type = BlockType(typ)
            block_color = BlockColor[color]
            block_surfaces = self._surface_manager.get_block_surfaces(block_type)
            goal_block = Block(block_color, (0, 0), block_surfaces[block_color], block_type)
            goals[(block_type, block_color)] = (c, goal_block)

        return goals

    def get_max_level(self):
        """
        Get the number of levels available
        :return:
        """
        return len(self.level_data)
