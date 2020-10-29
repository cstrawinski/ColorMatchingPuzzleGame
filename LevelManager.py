from Block import Block
import json


class LevelManager:
    def __init__(self):
        self.level_data = []
        self.goals = []

    def save(self):
        with open('leveldata.json', 'w') as f:
            json.dump(self.level_data, f)

    def load(self):
        with open('leveldata.json', 'r') as f:
            self.level_data = json.load(f)

    def get_goals(self, level):
        goal_data = self.level_data[level]['goal']
        # self.goals = [Block(color, (0, 0),  for c, typ, color in goal_data)]
