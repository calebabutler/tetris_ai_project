#!/usr/bin/env python3

# Copyright (c) 2023 Charleston Andrews, Caleb Butler
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from tetris_game import TetrisGame, Piece, Color
import numpy as np
import pygame

BLOCK_SIZE = 20


class Renderer:
    '''
    This class is a companion to the TetrisGame class. It creates a pygame
    window that visually shows the user the current state of a TetrisGame
    object.
    '''

    def __init__(self, game: TetrisGame) -> None:
        self.game = game

    def get_game(self) -> TetrisGame:
        '''
        Getter for game object
        '''
        return self.game

    def set_game(self, game: TetrisGame) -> None:
        '''
        Setter for game object
        '''
        self.game = game

    def setup(self) -> None:
        '''
        Run this function to render the first frame
        '''
        pygame.init()
        self.screen = pygame.display.set_mode((16 * BLOCK_SIZE,
                                               30 * BLOCK_SIZE))
        self.font = pygame.freetype.Font('LiberationSans-Regular.ttf', 12)
        self.rerender()

    def rerender(self) -> None:
        '''
        Run this function to render successive frames
        '''
        self.screen.fill((0, 0, 0))
        self.screen.fill((50, 50, 50),
                         pygame.Rect(10 * BLOCK_SIZE, 0, 6 * BLOCK_SIZE,
                                     30 * BLOCK_SIZE))
        self.screen.fill((50, 50, 50),
                         pygame.Rect(0, 0, 10 * BLOCK_SIZE, 9 * BLOCK_SIZE))
        self._render_level()
        self._render_score()
        self._render_game_over()
        self._render_game_aggregate_height()
        self._render_game_holes()
        self._render_game_bumpiness()        
        self._render_shadow_piece()
        self._render_current_piece()
        self._render_next_pieces()
        self._render_hold_piece()
        self._render_board()
        pygame.display.flip()

    def _render_block(self, position: np.ndarray, color: int,
                      offset: np.ndarray = np.array([0, 0]),
                      alpha: int = 0) -> None:
        position += offset
        rect = pygame.Rect(position[0] * BLOCK_SIZE,
                           (position[1] - 10) * BLOCK_SIZE,
                           BLOCK_SIZE, BLOCK_SIZE)
        match color:
            case Color.BLANK.value:
                pass
            case Color.LIGHT_BLUE.value:
                self.screen.fill((0, 255 - alpha, 255 - alpha), rect)
            case Color.DARK_BLUE.value:
                self.screen.fill((0, 0, 255 - alpha), rect)
            case Color.ORANGE.value:
                self.screen.fill((255 - alpha, 127 - alpha // 2, 0), rect)
            case Color.YELLOW.value:
                self.screen.fill((255 - alpha, 255 - alpha, 0), rect)
            case Color.GREEN.value:
                self.screen.fill((0, 255 - alpha, 0), rect)
            case Color.RED.value:
                self.screen.fill((255 - alpha, 0, 0), rect)
            case Color.MAGENTA.value:
                self.screen.fill((128 - alpha // 2, 0, 128 - alpha // 2), rect)

    def _render_any_board(self, board: np.ndarray,
                          offset: np.ndarray = np.array([0, 0]),
                          alpha: int = 0):
        for i in range(19, 40):
            for j in range(10):
                self._render_block(np.array([j, i]), board[i][j], offset,
                                   alpha)

    def _render_piece(self, piece: Piece,
                      offset: np.ndarray = np.array([0, 0]),
                      alpha: int = 0) -> None:
        _, board = self.game.convert_piece_to_board(piece)
        self._render_any_board(board, offset, alpha)

    def _render_current_piece(self) -> None:
        self._render_piece(self.game.get_current_piece())

    def _render_shadow_piece(self) -> None:
        self._render_piece(self.game.get_shadow_piece(), alpha=100)

    def _render_next_pieces(self) -> None:
        next_pieces = self.game.get_next_pieces()
        for i, kind in enumerate(next_pieces):
            piece = Piece(kind, np.array([2, 38]), 0)
            self._render_piece(piece, offset=np.array([11, -25 + i * 4]))

    def _render_hold_piece(self) -> None:
        kind = self.game.get_hold_piece()
        if kind >= 0:
            piece = Piece(kind, np.array([2, 38]), 0)
            self._render_piece(piece, offset=np.array([11, 0]))

    def _render_board(self) -> None:
        self._render_any_board(self.game.get_board())

    def _render_level(self) -> None:
        self.font.render_to(self.screen, (10, 10),
                            f'Level: {self.game.get_level()}', (255, 255, 255))

    def _render_score(self) -> None:
        self.font.render_to(self.screen, (10, 28),
                            f'Score: {self.game.get_score()}', (255, 255, 255))

    def _render_game_over(self) -> None:
        self.font.render_to(self.screen, (10, 46),
                            f'Game over?: {self.game.is_over()}',
                            (255, 255, 255))
    
    def _render_game_aggregate_height(self) -> None:
        self.font.render_to(self.screen, (10, 64),
                            f'Aggregate Height: {self.game.get_aggregate_height()}', (255, 255, 255))
        
    def _render_game_holes(self) -> None:
        self.font.render_to(self.screen, (10, 82),
                            f'Number of Holes: {self.game.get_number_holes()}', (255, 255, 255))  

    def _render_game_bumpiness(self) -> None:
        self.font.render_to(self.screen, (10, 100),
                            f'Bumpiness: {self.game.get_bumpiness()}', (255, 255, 255))  