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

from tetris_game import TetrisGame, Piece, pieces, Color
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
        self._render_shadow_piece()
        self._render_current_piece()
        self._render_next_pieces()
        self._render_hold_piece()
        self._render_board()
        pygame.display.flip()

    def _render_block(self, position: np.ndarray, color: int,
                      on_board: bool, alpha: int = 0) -> None:
        if position[1] < 19 and on_board:
            return
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

    def _render_piece(self, piece: Piece, on_board: bool,
                      alpha: int = 0) -> None:
        assert piece.kind >= 0 and piece.kind < len(pieces)
        piece_size = len(pieces[piece.kind][0])
        piece_grid = pieces[piece.kind][piece.rotation]
        match piece_size:
            case 2:
                for k in range(4):
                    self._render_block(
                            piece.position + np.array([k % 2 - 1, k // 2 - 2]),
                            piece_grid[k // 2][k % 2], on_board, alpha)
            case 3:
                for k in range(9):
                    self._render_block(
                            piece.position + np.array([k % 3 - 2, k // 3 - 2]),
                            piece_grid[k // 3][k % 3], on_board, alpha)
            case 4:
                for k in range(16):
                    self._render_block(
                            piece.position + np.array([k % 4 - 2, k // 4 - 2]),
                            piece_grid[k // 4][k % 4], on_board, alpha)

    def _render_current_piece(self) -> None:
        self._render_piece(self.game.get_current_piece(), True)

    def _render_shadow_piece(self) -> None:
        self._render_piece(self.game.get_shadow_piece(), True, 100)

    def _render_next_pieces(self) -> None:
        next_pieces = self.game.get_next_pieces()
        for i in range(len(next_pieces)):
            self._render_piece(Piece(next_pieces[i],
                                     np.array([13, 13 + i * 4]), 0),
                               False)

    def _render_hold_piece(self) -> None:
        hold_piece = self.game.get_hold_piece()
        if hold_piece >= 0:
            self._render_piece(Piece(hold_piece,
                                     np.array([13, 37]), 0), False)

    def _render_board(self) -> None:
        board = self.game.get_board()
        for i in range(19, 40):
            for j in range(10):
                self._render_block(np.array([j, i]), board[i][j], True)

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
