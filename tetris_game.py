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

from typing import Self
from enum import Enum
from dataclasses import dataclass
import copy
import random

pieces = [
    [
        [
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [1, 1, 1, 1],
            [0, 0, 0, 0],
        ],
        [
            [0, 1, 0, 0],
            [0, 1, 0, 0],
            [0, 1, 0, 0],
            [0, 1, 0, 0],
        ],
        [
            [0, 0, 0, 0],
            [1, 1, 1, 1],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
        ],
        [
            [0, 0, 1, 0],
            [0, 0, 1, 0],
            [0, 0, 1, 0],
            [0, 0, 1, 0],
        ],
    ],
    [
        [
            [0, 0, 0],
            [2, 0, 0],
            [2, 2, 2],
        ],
        [
            [2, 2, 0],
            [2, 0, 0],
            [2, 0, 0],
        ],
        [
            [2, 2, 2],
            [0, 0, 2],
            [0, 0, 0],
        ],
        [
            [0, 0, 2],
            [0, 0, 2],
            [0, 2, 2],
        ],
    ],
    [
        [
            [0, 0, 0],
            [0, 0, 3],
            [3, 3, 3],
        ],
        [
            [3, 0, 0],
            [3, 0, 0],
            [3, 3, 0],
        ],
        [
            [3, 3, 3],
            [3, 0, 0],
            [0, 0, 0],
        ],
        [
            [0, 3, 3],
            [0, 0, 3],
            [0, 0, 3],
        ],
    ],
    [
        [
            [4, 4],
            [4, 4],
        ],
        [
            [4, 4],
            [4, 4],
        ],
        [
            [4, 4],
            [4, 4],
        ],
        [
            [4, 4],
            [4, 4],
        ],
    ],
    [
        [
            [0, 0, 0],
            [0, 5, 5],
            [5, 5, 0],
        ],
        [
            [5, 0, 0],
            [5, 5, 0],
            [0, 5, 0],
        ],
        [
            [0, 5, 5],
            [5, 5, 0],
            [0, 0, 0],
        ],
        [
            [0, 5, 0],
            [0, 5, 5],
            [0, 0, 5],
        ],
    ],
    [
        [
            [0, 0, 0],
            [6, 6, 0],
            [0, 6, 6],
        ],
        [
            [0, 6, 0],
            [6, 6, 0],
            [6, 0, 0],
        ],
        [
            [6, 6, 0],
            [0, 6, 6],
            [0, 0, 0],
        ],
        [
            [0, 0, 6],
            [0, 6, 6],
            [0, 6, 0],
        ],
    ],
    [
        [
            [0, 0, 0],
            [0, 7, 0],
            [7, 7, 7],
        ],
        [
            [7, 0, 0],
            [7, 7, 0],
            [7, 0, 0],
        ],
        [
            [7, 7, 7],
            [0, 7, 0],
            [0, 0, 0],
        ],
        [
            [0, 0, 7],
            [0, 7, 7],
            [0, 0, 7],
        ],
    ],
]


class Color(Enum):
    BLANK = 0
    LIGHT_BLUE = 1
    DARK_BLUE = 2
    ORANGE = 3
    YELLOW = 4
    GREEN = 5
    RED = 6
    MAGENTA = 7


class Input(Enum):
    NONE = 0
    C_ROTATE = 1
    CC_ROTATE = 2
    MOVE_LEFT = 3
    MOVE_RIGHT = 4
    SOFT_DROP = 5
    HARD_DROP = 6
    HOLD = 7


@dataclass
class Piece:
    kind: int
    position: (int, int)
    rotation: int


class TetrisGame:
    '''
    This class should be self-contained; meaning it does not rely on pygame or
    any other library. It should be automatable, meaning the user should be
    able to set its own inputs or steps. There should be 60 steps (or updates)
    in a second (preferably, framerate can be set).
    '''

    def __init__(self: Self, frame_rate: int) -> None:
        assert frame_rate > 0
        self.frame_rate = frame_rate
        self.next_input = Input.NONE.value
        self.level = 1
        self.waited_frames = 0
        self.hold_piece = -1
        self.can_hold = True
        self.piece_queue = []
        self.is_game_over = False
        self.board = []
        self.soft_drop_mode = False
        for i in range(40):
            self.board.append([])
            for j in range(10):
                self.board[i].append(Color.BLANK.value)
        self._generate_new_piece()

    def get_board(self: Self) -> [[int]]:
        '''
        Returns current board. Board data structure: 2D array with color
        information for the player, probably color information will be removed
        when read by the AI.
        '''
        return self.board

    def get_simple_board(self: Self) -> [[int]]:
        '''
        This function returns a binary board (no color information) that is
        21x10 with the current piece also included on the board.
        '''
        new_board = copy.deepcopy(self.board)
        for i in range(19):
            new_board.pop(0)
        for i in range(21):
            for j in range(10):
                if new_board[i][j] != 0:
                    new_board[i][j] = 1

        piece_size = len(pieces[self.piece.kind][0])
        x_pos = self.piece.position[0]
        y_pos = self.piece.position[1]
        piece_grid = pieces[self.piece.kind][self.piece.rotation]
        match piece_size:
            case 2:
                for k in range(4):
                    abs_x = x_pos + k % 2 - 1
                    abs_y = y_pos + k // 2 - 1
                    if abs_y >= 19 and piece_grid[k // 2][k % 2] != 0:
                        new_board[abs_y - 19][abs_x] = 1
            case 3:
                for k in range(9):
                    abs_x = x_pos + k % 3 - 2
                    abs_y = y_pos + k // 3 - 2
                    if abs_y >= 19 and piece_grid[k // 3][k % 3] != 0:
                        new_board[abs_y - 19][abs_x] = 1
            case 4:
                for k in range(16):
                    abs_x = x_pos + k % 4 - 2
                    abs_y = y_pos + k // 4 - 2
                    if abs_y >= 19 and piece_grid[k // 4][k % 4] != 0:
                        new_board[abs_y - 19][abs_x] = 1
        return new_board

    def get_frame_rate(self: Self) -> int:
        return self.frame_rate

    def get_shadow_piece(self: Self) -> Piece:
        new_piece = copy.deepcopy(self.piece)
        while not self._has_collision(new_piece):
            x = new_piece.position[0]
            y = new_piece.position[1]
            new_piece.position = (x, y + 1)
        x = new_piece.position[0]
        y = new_piece.position[1]
        new_piece.position = (x, y - 1)
        return new_piece

    def get_current_piece(self: Self) -> Piece:
        '''
        Returns piece and position/rotation
        '''
        return self.piece

    def get_next_pieces(self: Self) -> [int]:
        return self.piece_queue[:6]

    def get_hold_piece(self: Self) -> int:
        return self.hold_piece

    def set_next_input(self: Self, next_input: int) -> None:
        '''
        Sets next input that will be registered after the next step
        '''
        self.next_input = next_input

    def is_over(self: Self) -> bool:
        '''
        Returns if the game is over or not
        '''
        return self.is_game_over

    def get_level(self: Self) -> int:
        return self.level

    def get_score(self: Self) -> int:
        return self.level

    def step(self: Self) -> None:
        '''
        Complete a next step
        '''
        if not self.is_game_over:
            self._process_next_input()
            self._apply_gravity()
            self._clear_lines()

    def _has_collision(self: Self, piece: Piece) -> bool:
        assert piece.kind >= 0 and piece.kind < len(pieces)
        piece_size = len(pieces[piece.kind][0])
        x_pos = piece.position[0]
        y_pos = piece.position[1]
        piece_grid = pieces[piece.kind][piece.rotation]
        match piece_size:
            case 2:
                for k in range(4):
                    if piece_grid[k // 2][k % 2] != Color.BLANK.value:
                        abs_x = x_pos + k % 2 - 1
                        abs_y = y_pos + k // 2 - 1
                        if abs_x < 0 or abs_x >= 10:
                            return True
                        if abs_y < 0 or abs_y >= 40:
                            return True
                        if self.board[abs_y][abs_x] != Color.BLANK.value:
                            return True
            case 3:
                for k in range(9):
                    if piece_grid[k // 3][k % 3] != Color.BLANK.value:
                        abs_x = x_pos + k % 3 - 2
                        abs_y = y_pos + k // 3 - 2
                        if abs_x < 0 or abs_x >= 10:
                            return True
                        if abs_y < 0 or abs_y >= 40:
                            return True
                        if self.board[abs_y][abs_x] != Color.BLANK.value:
                            return True
            case 4:
                for k in range(16):
                    if piece_grid[k // 4][k % 4] != Color.BLANK.value:
                        abs_x = x_pos + k % 4 - 2
                        abs_y = y_pos + k // 4 - 2
                        if abs_x < 0 or abs_x >= 10:
                            return True
                        if abs_y < 0 or abs_y >= 40:
                            return True
                        if self.board[abs_y][abs_x] != Color.BLANK.value:
                            return True
        return False

    def _process_next_input(self: Self) -> None:
        new_piece = copy.deepcopy(self.piece)
        match self.next_input:
            case Input.NONE.value:
                pass
            case Input.C_ROTATE.value:
                new_piece.rotation += 1
                new_piece.rotation %= 4
            case Input.CC_ROTATE.value:
                new_piece.rotation += 3
                new_piece.rotation %= 4
            case Input.MOVE_LEFT.value:
                pos = new_piece.position
                x = pos[0]
                y = pos[1]
                new_piece.position = (x - 1, y)
            case Input.MOVE_RIGHT.value:
                pos = new_piece.position
                x = pos[0]
                y = pos[1]
                new_piece.position = (x + 1, y)
            case Input.SOFT_DROP.value:
                self.soft_drop_mode = not self.soft_drop_mode
            case Input.HARD_DROP.value:
                self.piece = self.get_shadow_piece()
                self._lock_piece()
                self.next_input = Input.NONE.value
                return
            case Input.HOLD.value:
                if self.can_hold:
                    if self.hold_piece >= 0:
                        tmp = self.piece.kind
                        self._generate_new_piece(self.hold_piece)
                        self.hold_piece = tmp
                    else:
                        self.hold_piece = self.piece.kind
                        self._generate_new_piece()
                    self.can_hold = False
                    self.next_input = Input.NONE.value
                    return
        if not self._has_collision(new_piece):
            self.piece = new_piece
        self.next_input = Input.NONE.value

    def _generate_new_piece(self: Self, specific_kind: int = -1) -> None:
        if len(self.piece_queue) <= 6:
            bag = list(range(7))
            random.shuffle(bag)
            self.piece_queue += bag
        if specific_kind < 0:
            new_piece = Piece(self.piece_queue.pop(0), (5, 19), 0)
        else:
            new_piece = Piece(specific_kind, (5, 19), 0)
        if self._has_collision(new_piece):
            self.is_game_over = True
            self.piece = Piece(0, (0, 2), 0)
        else:
            self.piece = new_piece
            self.can_hold = True
            self.soft_drop_mode = False

    def _lock_piece(self: Self) -> None:
        piece_size = len(pieces[self.piece.kind][0])
        x_pos = self.piece.position[0]
        y_pos = self.piece.position[1]
        piece_grid = pieces[self.piece.kind][self.piece.rotation]
        match piece_size:
            case 2:
                for k in range(4):
                    if piece_grid[k // 2][k % 2] != Color.BLANK.value:
                        abs_x = x_pos + k % 2 - 1
                        abs_y = y_pos + k // 2 - 1
                        self.board[abs_y][abs_x] = piece_grid[k // 2][k % 2]
            case 3:
                for k in range(9):
                    if piece_grid[k // 3][k % 3] != Color.BLANK.value:
                        abs_x = x_pos + k % 3 - 2
                        abs_y = y_pos + k // 3 - 2
                        self.board[abs_y][abs_x] = piece_grid[k // 3][k % 3]
            case 4:
                for k in range(16):
                    if piece_grid[k // 4][k % 4] != Color.BLANK.value:
                        abs_x = x_pos + k % 4 - 2
                        abs_y = y_pos + k // 4 - 2
                        self.board[abs_y][abs_x] = piece_grid[k // 4][k % 4]
        self._generate_new_piece()

    def _apply_gravity(self: Self) -> None:
        G = (0.8 - (self.level - 1) * 0.007)**(self.level - 1)

        if self.soft_drop_mode and G > 0.05:
            G = 0.05

        G_frames = G * self.frame_rate
        self.waited_frames += 1
        if self.waited_frames >= G_frames:
            new_piece = copy.deepcopy(self.piece)
            self.waited_frames = 0
            pos = new_piece.position
            x = pos[0]
            y = pos[1]
            new_piece.position = (x, y + 1)
            if self._has_collision(new_piece):
                self._lock_piece()
            else:
                self.piece = new_piece

    def _clear_lines(self: Self) -> None:
        for i in range(len(self.board)):
            full = True
            for j in range(len(self.board[i])):
                if self.board[i][j] == Color.BLANK.value:
                    full = False
                    break
            if full:
                new_line = [0] * 10
                self.board.pop(i)
                self.board.insert(0, new_line)
                self.level += 1
