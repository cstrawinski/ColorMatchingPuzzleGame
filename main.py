import pygame
import sys
from pygame.locals import *
from colors import *
from Board import Board
from LevelManager import LevelManager


# Lets make our entry point a class, cause why not?
class Game:
    WINDOW_SIZE = (400, 480)

    def __init__(self):
        pygame.init()
        self._animation_timer = pygame.time.Clock()
        self._window_surface = pygame.display.set_mode(self.WINDOW_SIZE, 0, 32)
        pygame.display.set_caption('Color Matching Puzzle Game')
        self._level_manager = LevelManager()
        self._game_board = Board((10, 12), (35, 80))
        self._level = 0
        self._score = 0
        self._remaining_moves = 0
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
                        self._execute_move(connected_blocks)

    def _execute_move(self, connected_blocks):
        self._game_board.clear(connected_blocks)
        self._score += len(connected_blocks)
        self._remaining_moves -= 1
        self._game_board.fill_empty_blocks(connected_blocks)

    def draw_stats(self):
        self.draw_score()
        self.draw_moves()

    def draw_moves(self):
        text = self._score_font.render('Moves: %s' % self._remaining_moves, True, WHITE)
        text_rect = text.get_rect()
        text_rect.x = self.WINDOW_SIZE[0] - 100
        self._window_surface.blit(text, text_rect)

    def draw_score(self):
        text = self._score_font.render('Score: %s' % self._score, True, WHITE)
        self._window_surface.blit(text, text.get_rect())

    def end_game(self):
        text = self._big_font.render('Game Over', True, WHITE)
        text_rect = text.get_rect()
        text_rect.centerx = self._window_surface.get_rect().centerx
        text_rect.centery = self._window_surface.get_rect().centery
        self._window_surface.fill(GRAY, text_rect.inflate(10, 10), BLEND_RGB_SUB)
        self._window_surface.blit(text, text_rect)

    def play(self):
        self._level_manager.load()
        self._game_board.new(self._level_manager.level_data[self._level])
        self._remaining_moves = self._level_manager.level_data[self._level]['max_moves']

        while True:
            self.__handle_events()

            self._window_surface.fill(BLACK)

            self._game_board.draw(self._window_surface)
            self.draw_stats()

            if self._remaining_moves <= 0:
                self.end_game()

            pygame.display.flip()
            self._animation_timer.tick(60)


if __name__ == '__main__':
    game = Game()
    game.play()
