import pygame
import sys
import Board
from pygame.locals import *
from colors import *


# Lets make our entry point a class, cause why not?
class Game:
    WINDOW_SIZE = (400, 480)

    def __init__(self):
        pygame.init()
        self._window_surface = pygame.display.set_mode(self.WINDOW_SIZE, 0, 32)
        pygame.display.set_caption('Color Matching Puzzle Game')
        self._game_board = Board.Board(10, 12, (35, 80))
        self._score = 0
        self._moves = 0
        self._score_font = pygame.font.SysFont(None, 24)

    def __handle_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                clicked_block = self._game_board.click_block(event.pos)
                if clicked_block is not None:
                    connected_blocks = self._game_board.get_connected_blocks(clicked_block, set())
                    if len(connected_blocks) >= 3:
                        self._game_board.clear(connected_blocks)
                        self._score += len(connected_blocks)
                        self._moves += 1
                        self._game_board.fill_empty_blocks(connected_blocks)

    def draw_stats(self):
        self.draw_score()
        self.draw_moves()

    def draw_moves(self):
        text = self._score_font.render('Moves: %s' % self._moves, True, WHITE)
        text_rect = text.get_rect()
        text_rect.x = self.WINDOW_SIZE[0] - 100
        self._window_surface.blit(text, text_rect)

    def draw_score(self):
        text = self._score_font.render('Score: %s' % self._score, True, WHITE)
        self._window_surface.blit(text, text.get_rect())

    def play(self):
        self._game_board.new()

        while True:
            self.__handle_events()

            self._window_surface.fill(BLACK)

            self._game_board.draw(self._window_surface)
            self.draw_stats()

            pygame.display.flip()


if __name__ == '__main__':
    game = Game()
    game.play()
