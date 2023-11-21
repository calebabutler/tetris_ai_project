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
from typing import Self
import pygame

BLOCK_SIZE = 20


class Renderer:

    def __init__(self: Self, game: TetrisGame) -> None:
        self.game = game

    def get_game(self: Self) -> TetrisGame:
        return self.game

    def setup(self: Self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((16 * BLOCK_SIZE,
                                               21 * BLOCK_SIZE))
        self.rerender()

    def _render_block(self: Self, position: (int, int), color: int) -> None:
        rect = pygame.Rect(position[0] * BLOCK_SIZE, position[1] * BLOCK_SIZE,
                           BLOCK_SIZE, BLOCK_SIZE)
        match color:
            case Color.BLANK.value:
                pass
            case Color.LIGHT_BLUE.value:
                self.screen.fill((0, 255, 255), rect)
            case Color.DARK_BLUE.value:
                self.screen.fill((0, 0, 255), rect)
            case Color.ORANGE.value:
                self.screen.fill((255, 127, 0), rect)
            case Color.YELLOW.value:
                self.screen.fill((255, 255, 0), rect)
            case Color.GREEN.value:
                self.screen.fill((0, 255, 0), rect)
            case Color.RED.value:
                self.screen.fill((255, 0, 0), rect)
            case Color.MAGENTA.value:
                self.screen.fill((128, 0, 128), rect)

    def _render_piece(self: Self, piece: Piece) -> None:
        assert piece.kind >= 0 and piece.kind < len(pieces)
        piece_size = len(pieces[piece.kind][0])
        x_pos = piece.position[0]
        y_pos = piece.position[1]
        piece_grid = pieces[piece.kind][piece.rotation]
        match piece_size:
            case 2:
                for k in range(4):
                    self._render_block((x_pos + k % 2 - 1, y_pos + k // 2 - 1),
                                       piece_grid[k // 2][k % 2])
            case 3:
                for k in range(9):
                    self._render_block((x_pos + k % 3 - 2, y_pos + k // 3 - 2),
                                       piece_grid[k // 3][k % 3])
            case 4:
                for k in range(16):
                    self._render_block((x_pos + k % 4 - 2, y_pos + k // 4 - 2),
                                       piece_grid[k // 4][k % 4])

    def _render_current_piece(self: Self) -> None:
        self._render_piece(self.game.get_current_piece())

    def _render_next_pieces(self: Self) -> None:
        pass

    def _render_hold_piece(self: Self) -> None:
        pass

    def _render_board(self: Self) -> None:
        pass

    def rerender(self: Self) -> None:
        self.screen.fill((0, 0, 0))
        self.screen.fill((50, 50, 50),
                         pygame.Rect(10 * BLOCK_SIZE, 0, 6 * BLOCK_SIZE,
                                     21 * BLOCK_SIZE))
        self._render_current_piece()
        self._render_next_pieces()
        self._render_hold_piece()
        self._render_board()
        pygame.display.flip()
