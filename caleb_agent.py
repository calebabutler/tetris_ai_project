from tetris_game import TetrisGame
from renderer import Renderer
from agent import DQNAgent
from simple_ai import move, get_utility
import numpy as np
import copy
import pygame


def get_state(game: TetrisGame) -> np.ndarray:
    state = np.zeros(41, dtype=int)
    state[0] = game.get_current_piece().kind
    board = game.get_board()
    for i, row in enumerate(board):
        n = 0
        for j, item in enumerate(row):
            if item != 0:
                n += 2**j
        state[i + 1] = n
    return state


def main() -> None:
    game = TetrisGame(60)
    renderer = Renderer(game)
    renderer.setup()
    agent = DQNAgent(41, 44)
    running = True
    game.step()
    renderer.rerender()
    current_state = get_state(game)

    rendering_ticks = 0
    render_frame_rate = 60

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        if pygame.time.get_ticks() > rendering_ticks:
            renderer.rerender()
            rendering_ticks += 1000 // render_frame_rate

        next_states = []
        for action in range(44):
            position = action // 4
            rotation = action % 4
            new_game = copy.deepcopy(game)
            move(new_game, position, rotation)
            new_game.step()
            next_states.append(get_state(new_game))

        best_state = agent.select_state(next_states)

        if game.is_over():
            agent.train(len(agent.memory))
            game.reset()

            print('***************************')
            print(f'EPSILON: {agent.epsilon}')
            print('***************************')
        else:
            # print("The best state is, ", best_state)
            for i, state in enumerate(next_states):
                if np.all(state == best_state):
                    best_action = i
                    break
            # print("The best action is ", best_action)
            # print(utility(game))
            agent.remember(current_state, best_state,
                           get_utility(game, best_action // 4,
                                       best_action % 4),
                           game.is_over())
            move(game, best_action // 4, best_action % 4)
            game.step()
            current_state = best_state


if __name__ == '__main__':
    main()
