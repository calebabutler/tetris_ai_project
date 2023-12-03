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
import numpy as np

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
class Piece:
    kind: int
    position: np.ndarray
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
        self.reset()

    def reset(self) -> None:
        '''
        Reset the game to the initial state
        '''
        self.successful_rotation = False
        self.next_input = Input.NONE.value
        self.level = 1
        self.score = 0
        self.waited_frames = 0
        self.hold_piece = -1
        self.can_hold = True
        self.piece_queue = []
        self.is_game_over = False
        self.board = np.zeros((40, 10), dtype=int)
        self.soft_drop_mode = False
        self.lock_mode = False
        self.lock_count = 0
        self.had_tetris = False
        self.t_spin = False
        self._generate_new_piece()
        ## Line 280/281 Addition Made by Charleston Andrews: 12/2/2023
        self.aggregate_height = 0
        self.bumpiness = 0
        self.number_holes = 0        

    def get_board(self) -> np.ndarray:
        '''
        Returns current board. Board data structure: 2D array with color
        information. The Color enum says which color correspond with which
        int.
        '''
        return self.board

    def convert_piece_to_board(self, piece: Piece) -> (bool, np.ndarray):
        '''
        Converts piece information to a board with only that piece. Returns a
        boolean saying if the conversion was successful.
        '''
        board = np.zeros((40, 10), dtype=int)
        success = True
        piece_size = len(pieces[piece.kind][0])
        piece_grid = pieces[piece.kind][piece.rotation]
        match piece_size:
            case 2:
                for k in range(4):
                    board_pos = piece.position + np.array([k % 2 - 1,
                                                           k // 2 - 2])
                    if piece_grid[k // 2][k % 2] != 0:
                        if (board_pos[1] < 0 or board_pos[1] >= 40
                                or board_pos[0] < 0 or board_pos[0] >= 10):
                            success = False
                            break
                        board[board_pos[1]][board_pos[0]] = (
                                piece_grid[k // 2][k % 2])
            case 3:
                for k in range(9):
                    board_pos = piece.position + np.array([k % 3 - 2,
                                                           k // 3 - 2])
                    if piece_grid[k // 3][k % 3] != 0:
                        if (board_pos[1] < 0 or board_pos[1] >= 40
                                or board_pos[0] < 0 or board_pos[0] >= 10):
                            success = False
                            break
                        board[board_pos[1]][board_pos[0]] = (
                                piece_grid[k // 3][k % 3])
            case 4:
                for k in range(16):
                    board_pos = piece.position + np.array([k % 4 - 2,
                                                           k // 4 - 2])
                    if piece_grid[k // 4][k % 4] != 0:
                        if (board_pos[1] < 0 or board_pos[1] >= 40
                                or board_pos[0] < 0 or board_pos[0] >= 10):
                            success = False
                            break
                        board[board_pos[1]][board_pos[0]] = (
                                piece_grid[k // 4][k % 4])
        return (success, board)

    def combine_boards(self, board1: np.ndarray, board2: np.ndarray) -> bool:
        '''
        Combines two boards into one. There cannot be any overlap between the
        two boards. This function returns a boolean saying whether the process
        was successful. Result is stored in the first board.
        '''
        if np.any(board1 * board2):
            return False
        board1 += board2
        return True

    def get_simple_board(self) -> np.ndarray:
        '''
        This function returns a binary board (no color information) that is
        21x10 with the current piece also included on the board.
        '''
        _, new_board = self.convert_piece_to_board(self.piece)
        self.combine_boards(new_board, self.board)
        new_board = new_board[19:]
        new_board[new_board != 0] = 1
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
            new_piece.position[1] += 1
        new_piece.position[1] -= 1
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
        success, new_board = self.convert_piece_to_board(piece)
        if not success:
            return True
        success = self.combine_boards(new_board, self.board)
        return not success

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
            new_new_piece.position += np.array([shift[0], -shift[1]])
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
            new_piece.position[0] += 1
        else:
            new_piece.position[0] -= 1
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
            new_piece = Piece(self.piece_queue.pop(0), np.array([5, 19]), 0)
        else:
            new_piece = Piece(specific_kind, np.array([5, 19]), 0)
        if self._has_collision(new_piece):
            self.is_game_over = True
            self.piece = Piece(0, np.array([0, 2]), 0)
        else:
            self.piece = new_piece
            self.can_hold = True
            self.soft_drop_mode = False

    def _lock_piece(self) -> None:
        # Recognize t-spin
        self.t_spin = False
        if self.successful_rotation and self.piece.kind == 6:
            occupied_squares = 0
            for i in range(4):
                board_pos = self.piece.position + np.array([2 * (i % 2) - 2,
                                                            2 * (i // 2) - 2])
                if (board_pos[1] < 0 or board_pos[1] >= 40
                        or board_pos[0] < 0 or board_pos[0] >= 10
                        or self.board[board_pos[1]][board_pos[0]]
                        != Color.BLANK.value):
                    occupied_squares += 1
            if occupied_squares >= 3:
                self.t_spin = True
        # Lock piece
        _, new_board = self.convert_piece_to_board(self.piece)
        self.combine_boards(self.board, new_board)
        # Line 550/551 Addition made by Charleston Andrews: 12/2/2023
        self.aggregate_height, self.bumpiness = self._calculate_aggregate_height_bumpiness()
        self.number_holes = self._calculate_number_holes()
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
                new_piece.position[1] += 1
                if self._has_collision(new_piece):
                    self.lock_mode = True
                else:
                    self.piece = new_piece
                    self.waited_frames = 0

    def _clear_lines(self) -> None:
        lines_cleared = 0
        for i in range(len(self.board)):
            if np.all(self.board[i]):
                lines_cleared += 1
                self.board = np.concatenate(
                        (np.zeros((1, 10), dtype=int),
                         np.roll(self.board, 1, axis=0)[1:i + 1],
                         self.board[i + 1:]))
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

    def _calculate_aggregate_height_bumpiness(self) -> (int, int):
        
        arr = self.get_board()
        column_height_array = [0] * 10
        column_check_array = [False] * 10
        count_x = 21
        count_y = 0

        for x in arr[19:]:
            count_y = 0
            for y in x:
                if(y > 0 and column_check_array[count_y]==False):
                    column_height_array[count_y] = count_x
                    column_check_array[count_y] = True
                count_y += 1
            count_x -= 1
        
        aggregate_height = 0
        bumpiness = 0
        temp = 0

        for z in range(0,10):
            aggregate_height += column_height_array[z]
        for z in range(0,9):
            temp = abs(column_height_array[z] - column_height_array[z+1])
            bumpiness += temp 
        return aggregate_height, bumpiness

    def get_aggregate_height(self) -> int:
        return self.aggregate_height

    def get_bumpiness(self) -> int:
        return self.bumpiness

    def _calculate_number_holes(self) -> int:
        arr = self.get_board()
        count_hole_array = [0] * 10
        column_array_previous = [0] * 10
        count_x = 21
        count_y = 0
        num_holes = 0
        for x in arr[19:]:
            if(count_x == 21):
                for y in x:
                    column_array_previous[count_y] = y
                    count_y += 1
                count_y = 0
            else:
                for y in x:
                    if(column_array_previous[count_y] > 0 and y == 0):
                        count_hole_array[y] += 1
                    column_array_previous[count_y] = y
                    count_y += 1
                count_y = 0
            count_x -= 1
        
        for z in range(0,10):
            num_holes += count_hole_array[z]
        return num_holes
   
    def get_number_holes(self) -> int:
        return self.number_holes

    def get_board_statistics(self):
        return [self.get_score(), self.get_number_holes(), self.get_bumpiness(), self.get_aggregate_height()]
    

    def get_next_state(self) -> None:
        states = {}
        piece_id = self.get_current_piece()
        if (piece_id.kind == 3):
            rotations = [0]
        elif(piece_id.kind == 0 or piece_id.kind == 4 or piece_id.kind == 5):
            rotations = [0,1]
        else:
            rotations = [0,1,2,3]
        
        piece = Piece(piece_id.kind,piece_id.position,piece_id.rotation)
    
                
    def position_lookuptable(self, piece: Piece) -> (int,int):
        min_x = 0
        max_x = 0
        match piece.kind:
            #Long Piece/Turquoise
            case 0:
                if (piece.rotation == 0):
                    min_x = 2
                    max_x = 8
                else:
                    min_x = 0
                    max_x = 9
            #L Piece/Blue
            case 1:
                if (piece.rotation == 0):
                    min_x = 2
                    max_x = 9
                elif (piece.rotation == 1):
                    min_x = 1
                    max_x = 9
                elif (piece.rotation == 2):
                    min_x = 2
                    max_x = 9
                else:
                    min_x = 2
                    max_x = 10
            #L Piece/Orange
            case 2:
                if (piece.rotation == 0):
                    min_x = 2
                    max_x = 9
                elif (piece.rotation == 1):
                    min_x = 1
                    max_x = 9
                elif (piece.rotation == 2):
                    min_x = 2
                    max_x = 9
                else:
                    min_x = 2
                    max_x = 10
            #Square Piece/Yellow
            case 3:
                min_x = 1
                max_x = 9
            #Skew Piece/Green
            case 4:
                if(piece.rotation == 0):
                    min_x = 2
                    max_x = 9
                else:
                    min_x = 1
                    max_x = 9
            #Skew Piece/Red
            case 5:
                if(piece.rotation == 0):
                    min_x = 2
                    max_x = 9
                else:
                    min_x = 2
                    max_x = 10
            #T Piece/Pink
            case 6:
                if(piece.rotation == 0):
                    min_x = 2
                    max_x = 9
                elif(piece.rotation == 1):
                    min_x = 1
                    max_x = 9
                elif(piece.rotation == 2):
                    min_x = 2
                    max_x = 9
                else:
                    min_x = 2
                    max_x = 10
            case _:
                min_x = 0
                max_x = 0
        return min_x,max_x
            





    


        

