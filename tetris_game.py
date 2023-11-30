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

from enum import Enum
from dataclasses import dataclass
import copy
import random

pieces = [
    [
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
    ],
    [
        [
            [2, 0, 0],
            [2, 2, 2],
            [0, 0, 0],
        ],
        [
            [0, 2, 2],
            [0, 2, 0],
            [0, 2, 0],
        ],
        [
            [0, 0, 0],
            [2, 2, 2],
            [0, 0, 2],
        ],
        [
            [0, 2, 0],
            [0, 2, 0],
            [2, 2, 0],
        ],
    ],
    [
        [
            [0, 0, 3],
            [3, 3, 3],
            [0, 0, 0],
        ],
        [
            [0, 3, 0],
            [0, 3, 0],
            [0, 3, 3],
        ],
        [
            [0, 0, 0],
            [3, 3, 3],
            [3, 0, 0],
        ],
        [
            [3, 3, 0],
            [0, 3, 0],
            [0, 3, 0],
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
            [0, 5, 5],
            [5, 5, 0],
            [0, 0, 0],
        ],
        [
            [0, 5, 0],
            [0, 5, 5],
            [0, 0, 5],
        ],
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
    ],
    [
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
    ],
    [
        [
            [0, 7, 0],
            [7, 7, 7],
            [0, 0, 0],
        ],
        [
            [0, 7, 0],
            [0, 7, 7],
            [0, 7, 0],
        ],
        [
            [0, 0, 0],
            [7, 7, 7],
            [0, 7, 0],
        ],
        [
            [0, 7, 0],
            [7, 7, 0],
            [0, 7, 0],
        ],
    ],
]

srs_table_clockwise = [
    [(0, 0), (-1, 0), (-1, -1), (0, 2), (-1, 2)],   # L->0
    [(0, 0), (-1, 0), (-1, 1), (0, -2), (-1, -2)],  # 0->R
    [(0, 0), (1, 0), (1, -1), (0, 2), (1, 2)],      # R->2
    [(0, 0), (1, 0), (1, 1), (0, -2), (1, -2)],     # 2->L
]

srs_table_counter_clockwise = [
    [(0, 0), (1, 0), (1, 1), (0, 2), (1, 2)],       # R->0
    [(0, 0), (-1, 0), (-1, 1), (0, -2), (-1, -2)],  # 2->R
    [(0, 0), (-1, 0), (-1, -1), (0, 2), (-1, 2)],   # L->2
    [(0, 0), (1, 0), (1, 1), (0, -2), (1, -2)],     # 0->L
]

srs_table_clockwise_I = [
    [(0, 0), (1, 0), (-2, 0), (1, -2), (-2, 1)],  # L->0
    [(0, 0), (-2, 0), (1, 0), (-2, -1), (1, 2)],  # 0->R
    [(0, 0), (-1, 0), (2, 0), (-1, 2), (2, -1)],  # R->2
    [(0, 0), (2, 0), (-1, 0), (2, 1), (-1, -2)],  # 2->L
]

srs_table_counter_clockwise_I = [
    [(0, 0), (2, 0), (-1, 0), (2, 1), (-1, -2)],  # R->0
    [(0, 0), (1, 0), (-2, 0), (1, -2), (-2, 1)],  # 2->R
    [(0, 0), (-2, 0), (1, 0), (-2, -1), (1, 2)],  # L->2
    [(0, 0), (-1, 0), (2, 0), (-1, 2), (2, -1)],  # 0->L
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
class Vector2x1:
    x: int
    y: int

    def __add__(self, other):
        return Vector2x1(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector2x1(self.x - other.x, self.y - other.y)


@dataclass
class Piece:
    kind: int
    position: Vector2x1
    rotation: int


class TetrisGame:
    '''
    This class holds all of the game logic for tetris, with no rendering logic
    or input handling logic. This means, if you want to automate playing
    tetris, you can use this class alone and just see the outcomes of the game
    logic. Use the Renderer class with this class to both run the game logic
    for the game and the rendering logic, with no input handling. See the
    'playable.py' file for a simple example of how to implement input handling.
    '''

    def __init__(self, frame_rate: int) -> None:
        assert frame_rate > 0
        self.frame_rate = frame_rate
        self.successful_rotation = False
        self.next_input = Input.NONE.value
        self.level = 1
        self.score = 0
        self.waited_frames = 0
        self.hold_piece = -1
        self.can_hold = True
        self.piece_queue = []
        self.is_game_over = False
        self.board = []
        self.soft_drop_mode = False
        self.lock_mode = False
        self.lock_count = 0
        self.had_tetris = False
        self.t_spin = False
        for i in range(40):
            self.board.append([])
            for j in range(10):
                self.board[i].append(Color.BLANK.value)
        self._generate_new_piece()

    def get_board(self) -> [[int]]:
        '''
        Returns current board. Board data structure: 2D array with color
        information. The Color enum says which color correspond with which
        int.
        '''
        return self.board

    def get_simple_board(self) -> [[int]]:
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
        piece_grid = pieces[self.piece.kind][self.piece.rotation]
        match piece_size:
            case 2:
                for k in range(4):
                    board_pos = self.piece.position + Vector2x1(k % 2 - 1,
                                                                k // 2 - 2)
                    if board_pos.y >= 19 and piece_grid[k // 2][k % 2] != 0:
                        new_board[board_pos.y - 19][board_pos.x] = 1
            case 3:
                for k in range(9):
                    board_pos = self.piece.position + Vector2x1(k % 3 - 2,
                                                                k // 3 - 2)
                    if board_pos.y >= 19 and piece_grid[k // 3][k % 3] != 0:
                        new_board[board_pos.y - 19][board_pos.x] = 1
            case 4:
                for k in range(16):
                    board_pos = self.piece.position + Vector2x1(k % 4 - 2,
                                                                k // 4 - 2)
                    if board_pos.y >= 19 and piece_grid[k // 4][k % 4] != 0:
                        new_board[board_pos.y - 19][board_pos.x] = 1
        return new_board

    def get_frame_rate(self) -> int:
        '''
        Return fixed frame rate
        '''
        return self.frame_rate

    def get_shadow_piece(self) -> Piece:
        '''
        Return piece information for the "shadow" of the current piece (that
        is, the dark piece that shows you where the piece would land)
        '''
        new_piece = copy.deepcopy(self.piece)
        while not self._has_collision(new_piece):
            new_piece.position += Vector2x1(0, 1)
        new_piece.position += Vector2x1(0, -1)
        return new_piece

    def get_current_piece(self) -> Piece:
        '''
        Returns current piece information
        '''
        return self.piece

    def get_next_pieces(self) -> [int]:
        '''
        Returns the kinds of the next 6 pieces
        '''
        return self.piece_queue[:6]

    def get_hold_piece(self) -> int:
        '''
        Returns the kind of the piece in hold
        '''
        return self.hold_piece

    def set_next_input(self, next_input: int) -> None:
        '''
        Sets next input that will be registered in the next step
        '''
        self.next_input = next_input

    def is_over(self) -> bool:
        '''
        Returns if the game is over or not
        '''
        return self.is_game_over

    def get_level(self) -> int:
        '''
        Returns current level
        '''
        return self.level

    def get_score(self) -> int:
        '''
        Returns current score
        '''
        return self.score

    def step(self) -> None:
        '''
        Run a 'step' (or frame) of the game
        '''
        if not self.is_game_over:
            self._process_next_input()
            self._apply_gravity()
            self._clear_lines()

    def _has_collision(self, piece: Piece) -> bool:
        assert piece.kind >= 0 and piece.kind < len(pieces)
        piece_size = len(pieces[piece.kind][0])
        piece_grid = pieces[piece.kind][piece.rotation]
        match piece_size:
            case 2:
                for k in range(4):
                    if piece_grid[k // 2][k % 2] != Color.BLANK.value:
                        board_pos = piece.position + Vector2x1(k % 2 - 1,
                                                               k // 2 - 2)
                        if board_pos.x < 0 or board_pos.x >= 10:
                            return True
                        if board_pos.y < 0 or board_pos.y >= 40:
                            return True
                        if (self.board[board_pos.y][board_pos.x]
                                != Color.BLANK.value):
                            return True
            case 3:
                for k in range(9):
                    if piece_grid[k // 3][k % 3] != Color.BLANK.value:
                        board_pos = piece.position + Vector2x1(k % 3 - 2,
                                                               k // 3 - 2)
                        if board_pos.x < 0 or board_pos.x >= 10:
                            return True
                        if board_pos.y < 0 or board_pos.y >= 40:
                            return True
                        if (self.board[board_pos.y][board_pos.x]
                                != Color.BLANK.value):
                            return True
            case 4:
                for k in range(16):
                    if piece_grid[k // 4][k % 4] != Color.BLANK.value:
                        board_pos = piece.position + Vector2x1(k % 4 - 2,
                                                               k // 4 - 2)
                        if board_pos.x < 0 or board_pos.x >= 10:
                            return True
                        if board_pos.y < 0 or board_pos.y >= 40:
                            return True
                        if (self.board[board_pos.y][board_pos.x]
                                != Color.BLANK.value):
                            return True
        return False

    def _rotate(self, is_clockwise: bool) -> None:
        new_piece = copy.deepcopy(self.piece)
        if is_clockwise:
            new_piece.rotation += 1
        else:
            new_piece.rotation += 3
        new_piece.rotation %= 4

        # Assign rotation table
        if new_piece.kind == 0:
            if is_clockwise:
                rotation_table = srs_table_clockwise_I[new_piece.rotation]
            else:
                rotation_table = (
                    srs_table_counter_clockwise_I[new_piece.rotation])
        elif is_clockwise:
            rotation_table = srs_table_clockwise[new_piece.rotation]
        else:
            rotation_table = (
                    srs_table_counter_clockwise[new_piece.rotation])

        for shift in rotation_table:
            new_new_piece = copy.deepcopy(new_piece)
            new_new_piece.position += Vector2x1(shift[0], -shift[1])
            if not self._has_collision(new_new_piece) and self.lock_count < 15:
                self.piece = new_new_piece
                if self.lock_mode:
                    self.lock_mode = False
                    self.lock_count += 1
                    self.waited_frames = 0
                self.successful_rotation = True
                break

    def _move_left_or_right(self, is_right: bool) -> None:
        new_piece = copy.deepcopy(self.piece)
        if is_right:
            new_piece.position += Vector2x1(1, 0)
        else:
            new_piece.position += Vector2x1(-1, 0)
        if not self._has_collision(new_piece) and self.lock_count < 15:
            self.piece = new_piece
            if self.lock_mode:
                self.lock_mode = False
                self.lock_count += 1
                self.waited_frames = 0

    def _process_next_input(self) -> None:
        match self.next_input:
            case Input.NONE.value:
                pass
            case Input.C_ROTATE.value:
                self._rotate(True)
            case Input.CC_ROTATE.value:
                self._rotate(False)
            case Input.MOVE_LEFT.value:
                self._move_left_or_right(False)
                self.successful_rotation = False
            case Input.MOVE_RIGHT.value:
                self._move_left_or_right(True)
                self.successful_rotation = False
            case Input.SOFT_DROP.value:
                self.soft_drop_mode = not self.soft_drop_mode
                self.successful_rotation = False
            case Input.HARD_DROP.value:
                self.piece = self.get_shadow_piece()
                self._lock_piece()
                self.lock_mode = False
                self.successful_rotation = False
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
                self.successful_rotation = False
        self.next_input = Input.NONE.value

    def _generate_new_piece(self, specific_kind: int = -1) -> None:
        if len(self.piece_queue) <= 6:
            bag = list(range(7))
            random.shuffle(bag)
            self.piece_queue += bag
        if specific_kind < 0:
            new_piece = Piece(self.piece_queue.pop(0), Vector2x1(5, 19), 0)
        else:
            new_piece = Piece(specific_kind, Vector2x1(5, 19), 0)
        if self._has_collision(new_piece):
            self.is_game_over = True
            self.piece = Piece(0, Vector2x1(0, 2), 0)
        else:
            self.piece = new_piece
            self.can_hold = True
            self.soft_drop_mode = False

    def _lock_piece(self) -> None:
        piece_size = len(pieces[self.piece.kind][0])
        piece_grid = pieces[self.piece.kind][self.piece.rotation]
        # Recognize t-spin
        self.t_spin = False
        if self.successful_rotation and self.piece.kind == 6:
            occupied_squares = 0
            for i in range(4):
                board_pos = self.piece.position + Vector2x1(2 * (i % 2) - 2,
                                                            2 * (i // 2) - 2)
                if (board_pos.y < 0 or board_pos.y >= 40
                        or board_pos.x < 0 or board_pos.x >= 10
                        or self.board[board_pos.y][board_pos.x]
                        != Color.BLANK.value):
                    occupied_squares += 1
            if occupied_squares >= 3:
                self.t_spin = True
        match piece_size:
            case 2:
                for k in range(4):
                    if piece_grid[k // 2][k % 2] != Color.BLANK.value:
                        board_pos = self.piece.position + Vector2x1(k % 2 - 1,
                                                                    k // 2 - 2)
                        self.board[board_pos.y][board_pos.x] = (
                                piece_grid[k // 2][k % 2])
            case 3:
                for k in range(9):
                    if piece_grid[k // 3][k % 3] != Color.BLANK.value:
                        board_pos = self.piece.position + Vector2x1(k % 3 - 2,
                                                                    k // 3 - 2)
                        self.board[board_pos.y][board_pos.x] = (
                                piece_grid[k // 3][k % 3])
            case 4:
                for k in range(16):
                    if piece_grid[k // 4][k % 4] != Color.BLANK.value:
                        board_pos = self.piece.position + Vector2x1(k % 4 - 2,
                                                                    k // 4 - 2)
                        self.board[board_pos.y][board_pos.x] = (
                                piece_grid[k // 4][k % 4])
        self._generate_new_piece()

    def _apply_gravity(self) -> None:
        if self.lock_mode:
            G = 0.5
        else:
            G = (0.8 - (self.level - 1) * 0.007)**(self.level - 1)
            if self.soft_drop_mode and G > 0.05:
                G = 0.05
        G_frames = G * self.frame_rate
        self.waited_frames += 1
        if self.waited_frames >= G_frames:
            if self.lock_mode:
                self._lock_piece()
                self.lock_count = 0
                self.lock_mode = False
            else:
                new_piece = copy.deepcopy(self.piece)
                new_piece.position += Vector2x1(0, 1)
                if self._has_collision(new_piece):
                    self.lock_mode = True
                else:
                    self.piece = new_piece
                    self.waited_frames = 0

    def _clear_lines(self) -> None:
        lines_cleared = 0
        for i in range(len(self.board)):
            full = True
            for j in range(len(self.board[i])):
                if self.board[i][j] == Color.BLANK.value:
                    full = False
                    break
            if full:
                lines_cleared += 1
                new_line = [0] * 10
                self.board.pop(i)
                self.board.insert(0, new_line)
        self._update_scores(lines_cleared)

    def _update_scores(self, lines_cleared: int) -> None:
        if lines_cleared == 0 and self.t_spin:
            self.score += 1
        elif lines_cleared == 1:
            if self.t_spin:
                self.score += 3
            else:
                self.score += 1
        elif lines_cleared == 2:
            if self.t_spin:
                self.score += 7
            else:
                self.score += 3
        elif lines_cleared == 3:
            if self.t_spin:
                self.score += 6
            else:
                self.score += 5
        elif lines_cleared == 4:
            if self.had_tetris:
                self.score += 12
            else:
                self.score += 8

        if lines_cleared == 4:
            self.had_tetris = True
        else:
            self.had_tetris = False

        self.t_spin = False
        if self.score >= self.level * (self.level + 1) // 2 * 5:
            self.level += 1
