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
from typing import Self
import pygame


class Playable:

    def __init__(self: Self, renderer: Renderer) -> None:
        self.renderer = renderer

    def run(self: Self) -> None:
        self.renderer.setup()
        running = True
        while running:
            self.renderer.rerender()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    match event.key:
                        case pygame.K_LEFT:
                            self.renderer.get_game().piece.rotation += 1
                            self.renderer.get_game().piece.rotation %= 4
                        case pygame.K_RIGHT:
                            self.renderer.get_game().piece.rotation += 3
                            self.renderer.get_game().piece.rotation %= 4
                        case pygame.K_SPACE:
                            self.renderer.get_game().piece.kind += 1
                            self.renderer.get_game().piece.kind %= 7
                        case pygame.K_w:
                            pos = self.renderer.get_game().piece.position
                            x = pos[0]
                            y = pos[1]
                            self.renderer.get_game().piece.position = (x,
                                                                       y - 1)
                        case pygame.K_s:
                            pos = self.renderer.get_game().piece.position
                            x = pos[0]
                            y = pos[1]
                            self.renderer.get_game().piece.position = (x,
                                                                       y + 1)
                        case pygame.K_a:
                            pos = self.renderer.get_game().piece.position
                            x = pos[0]
                            y = pos[1]
                            self.renderer.get_game().piece.position = (x - 1,
                                                                       y)
                        case pygame.K_d:
                            pos = self.renderer.get_game().piece.position
                            x = pos[0]
                            y = pos[1]
                            self.renderer.get_game().piece.position = (x + 1,
                                                                       y)


def main() -> None:
    game = TetrisGame(60)
    renderer = Renderer(game)
    playable = Playable(renderer)
    playable.run()


if __name__ == '__main__':
    main()
