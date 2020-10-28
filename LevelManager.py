import json


class LevelManager:
    def __init__(self):
        self.level_data = [{'level': 1, 'max_moves': 10, 'board_width': 10, 'board_height': 12, 'level_data': [(5, 5, 3)]},
                           {'level': 2, 'max_moves': 10, 'board_width': 10, 'board_height': 12, 'level_data': [(4, 5, 3), (5, 5, 3), (6, 5, 3)]}]

    def save(self):
        with open('leveldata.json', 'w') as f:
            json.dump(self.level_data, f)

    def load(self):
        with open('leveldata.json', 'r') as f:
            self.level_data = json.load(f)
