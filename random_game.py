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

from tetris_game import TetrisGame
from renderer import Renderer
import pygame
import random


def main() -> None:
    game = TetrisGame(60)
    renderer = Renderer(game)
    renderer.setup()
    running = True

    rendering_ticks = 0
    render_frame_rate = 60

    while running:
        game.step()
        if pygame.time.get_ticks() > rendering_ticks:
            renderer.rerender()
            rendering_ticks += 1000 // render_frame_rate
        game.set_next_input(random.randint(0, 8))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        if game.is_over():
            game.reset()


if __name__ == '__main__':
    main()
