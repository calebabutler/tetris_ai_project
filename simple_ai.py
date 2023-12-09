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

from tetris_game import TetrisGame, Input
from renderer import Renderer
import pygame
import copy
import numpy as np
import random
import sys


def move(game: TetrisGame, absolute_position: int, rotation: int,
         renderer: Renderer = None, clock: pygame.time.Clock = None) -> None:
    last_rotation = 100
    current_rotation = game.get_current_piece().rotation
    while (game.get_current_piece().rotation != rotation
           and last_rotation != current_rotation):
        game.set_next_input(Input.C_ROTATE.value)
        game.step()
        if renderer is not None:
            renderer.rerender()
            if clock is not None:
                clock.tick(game.get_frame_rate())
        last_rotation = current_rotation
        current_rotation = game.get_current_piece().rotation

    last_position = 100
    current_position = game.get_current_piece().position[0]
    while (current_position > absolute_position
           and last_position != current_position):
        game.set_next_input(Input.MOVE_LEFT.value)
        game.step()
        if renderer is not None:
            renderer.rerender()
            if clock is not None:
                clock.tick(game.get_frame_rate())
        last_position = current_position
        current_position = game.get_current_piece().position[0]

    last_position = 100
    current_position = game.get_current_piece().position[0]
    while (current_position < absolute_position
           and last_position != current_position):
        game.set_next_input(Input.MOVE_RIGHT.value)
        game.step()
        if renderer is not None:
            renderer.rerender()
            if clock is not None:
                clock.tick(game.get_frame_rate())
        last_position = current_position
        current_position = game.get_current_piece().position[0]

    game.set_next_input(Input.HARD_DROP.value)
    game.step()


def get_utility(game: TetrisGame, position: int, rotation: int, w_1: int,
                w_2: int, w_3: int) -> float:
    old_bumpiness = game.get_bumpiness()
    old_holes = game.get_number_holes()
    old_height = game.get_aggregate_height()
    old_score = game.get_score()

    new_game = copy.deepcopy(game)
    move(new_game, position, rotation)

    new_bumpiness = new_game.get_bumpiness()
    new_holes = new_game.get_number_holes()
    new_height = new_game.get_aggregate_height()
    new_score = new_game.get_score()

    bumpiness_delta = new_bumpiness - old_bumpiness
    holes_delta = new_holes - old_holes
    height_delta = new_height - old_height
    score_delta = new_score - old_score

    utility = (1000 * score_delta - w_1 * holes_delta - w_2 * bumpiness_delta
               - w_3 * height_delta)
    return utility


def get_next_move(game: TetrisGame, w_1: int, w_2: int,
                  w_3: int) -> (int, int):
    next_actions = []
    for i in range(11):
        for j in range(4):
            next_actions.append((i, j))

    # Don't favor any particular move when utility is equal
    random.shuffle(next_actions)

    max_utility = -np.inf
    for action in next_actions:
        utility = get_utility(game, action[0], action[1], w_1, w_2, w_3)
        if utility > max_utility:
            max_utility = utility
            best_action = action
    return best_action


def main(args: [str]) -> None:
    # Starting weights
    # Currently best weights found so far
    w_1 = 6
    w_2 = 1
    w_3 = 1

    if len(args) > 1 and args[1] == 'train':
        score_table = {}
        score_total = 0
        games = 0
        print((w_1, w_2, w_3))

    game = TetrisGame(60)
    renderer = Renderer(game)
    renderer.setup()
    running = True

    clock = pygame.time.Clock()

    while running:
        position, rotation = get_next_move(game, w_1, w_2, w_3)
        renderer.rerender()
        clock.tick(game.get_frame_rate())
        move(game, position, rotation, renderer, clock)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        if game.is_over():
            if len(args) > 1 and args[1] == 'train':
                games += 1
                score_total += game.get_score()
                if games >= 12:
                    score_table[(w_1, w_2, w_3)] = score_total
                    new_weights = max(score_table, key=score_table.get)
                    while (w_1, w_2, w_3) in score_table:
                        w_1 = max(1, new_weights[0] + random.randint(-10, 10))
                        w_2 = max(1, new_weights[1] + random.randint(-10, 10))
                        w_3 = max(1, new_weights[2] + random.randint(-10, 10))
                    print((w_1, w_2, w_3))
                    print(f'Best weights: {new_weights}')
                    print(
                        f'With average score: {score_table[new_weights] / 12}')
                    games = 0
                    score_total = 0
            game.reset()
        clock.tick(game.get_frame_rate())


if __name__ == '__main__':
    main(sys.argv)
