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


def main() -> None:
    game = TetrisGame(60)
    renderer = Renderer(game)
    renderer.setup()
    running = True

    clock = pygame.time.Clock()

    while running:
        game.step()
        renderer.rerender()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                match event.key:
                    case pygame.K_LEFT:
                        game.set_next_input(Input.MOVE_LEFT.value)
                    case pygame.K_RIGHT:
                        game.set_next_input(Input.MOVE_RIGHT.value)
                    case pygame.K_DOWN:
                        game.set_next_input(Input.SOFT_DROP.value)
                    case pygame.K_SPACE:
                        game.set_next_input(Input.HARD_DROP.value)
                    case pygame.K_c:
                        game.set_next_input(Input.HOLD.value)
                    case pygame.K_x:
                        game.set_next_input(Input.C_ROTATE.value)
                    case pygame.K_z:
                        game.set_next_input(Input.CC_ROTATE.value)
        clock.tick(game.get_frame_rate())


if __name__ == '__main__':
    main()
