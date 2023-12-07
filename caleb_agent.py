from tetris_game import TetrisGame
from renderer import Renderer
from agent import DQNAgent
import numpy as np
import copy
import pygame


previous_score = 0
previous_drops = 0
previous_bumpiness = 0
previous_height = 0
previous_holes = 0


def utility(game: TetrisGame) -> float:
    global previous_score, previous_drops, previous_bumpiness
    global previous_height, previous_holes
    scores_delta = game.get_score() - previous_score
    drops_delta = game.get_drops() - previous_drops
    bumpiness_delta = game.get_bumpiness() - previous_bumpiness
    height_delta = game.get_aggregate_height() - previous_height
    holes_delta = game.get_number_holes() - previous_holes
    previous_score = game.get_score()
    previous_drops = game.get_drops()
    previous_bumpiness = game.get_bumpiness()
    previous_height = game.get_aggregate_height()
    previous_holes = game.get_number_holes()
    terms = [1000*scores_delta, 10*drops_delta,
             -1*bumpiness_delta,
             -1*height_delta,
             -100*holes_delta]
    return sum(terms)


def get_state(game: TetrisGame) -> np.ndarray:
    state = np.zeros(21, dtype=int)
    board = game.get_simple_board()
    for i, row in enumerate(board):
        n = 0
        for j, item in enumerate(row):
            if item != 0:
                n += 2**j
        state[i] = n
    return state


def main() -> None:
    global previous_score, previous_drops, previous_bumpiness
    global previous_height, previous_holes

    game = TetrisGame(60)
    renderer = Renderer(game)
    renderer.setup()
    agent = DQNAgent(21, 7)
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
        for action in range(7):
            new_game = copy.deepcopy(game)
            new_game.set_next_input(action)
            new_game.step()
            next_states.append(get_state(new_game))
            best_state = agent.select_state(next_states)

            if game.is_over():
                agent.train(len(agent.memory))
                game.reset()

                previous_score = 0
                previous_drops = 0
                previous_bumpiness = 0
                previous_height = 0
                previous_holes = 0

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
                game.set_next_input(best_action)
                game.step()
                # print(utility(game))
                agent.remember(current_state, best_state, utility(game),
                               game.is_over())
                current_state = best_state


if __name__ == '__main__':
    main()
