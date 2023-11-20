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
    C_ROTATE = 0
    CC_ROTATE = 1
    MOVE_LEFT = 2
    MOVE_RIGHT = 3
    SOFT_DROP = 4
    HARD_DROP = 5
    HOLD = 6


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

    def __init__(self: Self, frame_rate: float) -> None:
        self.frame_rate = frame_rate

    def get_board(self: Self) -> [[int]]:
        '''
        Returns current board. Board data structure: 2D array with color
        information for the player, probably color information will be removed
        when read by the AI.
        '''
        pass

    def get_current_piece(self: Self) -> Piece:
        '''
        Returns piece and position/rotation
        '''
        return Piece(6, (10, 10), 0)

    def set_next_input(self: Self, next_input: int) -> None:
        '''
        Sets next input that will be registered after the next step
        '''
        pass

    def is_over(self: Self) -> bool:
        '''
        Returns if the game is over or not
        '''
        pass

    def step(self: Self) -> None:
        '''
        Complete a next step
        '''
        pass
