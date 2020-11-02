import os
import pygame
import sys
from pygame.locals import *
from colors import *
from Block import Block
from Board import Board
from LevelManager import LevelManager
from SurfaceManager import SurfaceManager


# Lets make our entry point a class, cause why not?
class Game:
    WINDOW_SIZE = (500, 600)
    HUD_SIZE = (WINDOW_SIZE[0], 80)

    def __init__(self):
        pygame.init()
        self._animation_timer = pygame.time.Clock()
        self._window_surface = pygame.display.set_mode(self.WINDOW_SIZE, 0, 32)
        pygame.display.set_caption('Color Matching Puzzle Game')
        self._surface_manager = SurfaceManager()
        self._level_manager = LevelManager(self._surface_manager)
        self._game_board = Board((10, 12), (35, self.HUD_SIZE[1]), self._surface_manager)
        self._level = 1
        self._score = 0
        self._remaining_moves = 0
        self._goals = {}
        self._score_font = pygame.font.SysFont(None, 24)
        self._big_font = pygame.font.SysFont(None, 48)

    def __handle_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN and event.button == 1 and self._remaining_moves > 0:
                clicked_block = self._game_board.click_block(event.pos)
                if clicked_block is not None:
                    connected_blocks = self._game_board.get_connected_blocks(clicked_block, set())
                    if len(connected_blocks) >= 3:
                        extra_cleared = self._game_board.check_adjacent_blocks(connected_blocks)
                        self._execute_move(self._game_board.get_block_at(clicked_block), connected_blocks, extra_cleared)

    def _execute_move(self, clicked_block, connected_blocks, extra_cleared):
        # Do we have a goal for these blocks?
        key = (clicked_block.get_block_type(), clicked_block.get_color())
        if key in self._goals:
            count, block = self._goals[key]
            count -= len(connected_blocks)
            if count < 0:
                count = 0
            self._goals[key] = count, block

        # Check goals of extra blocks cleared
        extra_coords = set()
        for b in extra_cleared:
            b_x, b_y, block = b
            extra_coords.add((b_x, b_y))
            key = (block.get_block_type(), block.get_color())
            if key in self._goals:
                count, block = self._goals[key]
                self._score += 1
                if count == 0:
                    continue
                self._goals[key] = count - 1, block

        self._game_board.clear(connected_blocks)
        self._score += len(connected_blocks)
        # No points for these, they were already counted
        if len(extra_coords) > 0:
            self._game_board.clear(extra_coords)
            connected_blocks.update(extra_coords)
        self._remaining_moves -= 1
        self._game_board.fill_empty_blocks(connected_blocks)

    def _new_level(self):
        level = self._level_manager.level_data[self._level - 1]

        # Position the board in the center of the window
        window_width, window_height = self.WINDOW_SIZE
        board_width = level['board_width'] * Block.SIZE[0]
        board_height = level['board_height'] * Block.SIZE[1]
        board_position = (window_width - board_width) / 2, (window_height - board_height) / 2

        self._game_board.new(self._level_manager.level_data[self._level - 1], board_position)
        self._remaining_moves = self._level_manager.level_data[self._level - 1]['max_moves']
        # self._level_manager.level_data[self._level]['goal']
        self._goals = self._level_manager.get_goals(self._level - 1)

    def _goals_completed(self):
        goals_passed = True
        for key, value in self._goals.items():
            count, block = value
            if count > 0:
                goals_passed = False
                break
        return goals_passed

    def draw_stats(self):
        self.draw_score()
        self.draw_moves()
        self.draw_goals()

    def draw_moves(self):
        text = self._score_font.render('Moves: %s' % self._remaining_moves, True, WHITE)
        text_rect = text.get_rect()
        text_rect.x = self.WINDOW_SIZE[0] - 90
        self._window_surface.blit(text, text_rect)

    def draw_score(self):
        text = self._score_font.render('Score: %s' % self._score, True, WHITE)
        self._window_surface.blit(text, text.get_rect())

    def draw_goals(self):
        hud_width, hud_height = self.HUD_SIZE
        temp_surface = pygame.Surface((hud_width, hud_height), 0, 32)
        total_width = 0
        height_offset = 5
        for (block_type, block_color), goal in self._goals.items():
            count, block = goal
            text = self._score_font.render('%s x ' % count, True, WHITE)
            temp_surface.blit(text, (total_width, 8 + height_offset))
            temp_surface.blit(block.get_image(), (total_width + text.get_rect().right, 0 + height_offset))
            total_width += (text.get_rect().right + Block.SIZE[0])
            # Add a wee bit of space between goals
            total_width += 5

        goal_surface = pygame.Surface((total_width, hud_height), 0, 32)
        goal_surface.blit(temp_surface, temp_surface.get_rect(), area=Rect((0, 0), (total_width, hud_height)))
        goal_rect = goal_surface.get_rect()
        goal_rect.centerx = self._window_surface.get_rect().centerx
        self._window_surface.blit(goal_surface, goal_rect)

    def end_game(self):
        text = self._big_font.render('Game Over', True, WHITE)
        text_rect = text.get_rect()
        text_rect.centerx = self._window_surface.get_rect().centerx
        text_rect.centery = self._window_surface.get_rect().centery
        self._window_surface.fill(GRAY, text_rect.inflate(10, 10), BLEND_RGB_SUB)
        self._window_surface.blit(text, text_rect)

    def win_level(self):
        if self._level < self._level_manager.get_max_level():
            self._level += 1

        self._new_level()

    def play(self):
        self._surface_manager.load_blocks(os.path.join("resources", "blocks.png"))
        self._level_manager.load()
        self._new_level()

        while True:
            self.__handle_events()

            self._window_surface.fill(BLACK)

            self._game_board.draw(self._window_surface)
            self.draw_stats()

            if self._remaining_moves <= 0:
                self.end_game()

            if self._goals_completed():
                self.win_level()

            pygame.display.flip()
            self._animation_timer.tick(60)


if __name__ == '__main__':
    game = Game()
    game.play()
