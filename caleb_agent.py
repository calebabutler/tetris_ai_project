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
    if (scores_delta < 0 or drops_delta < 0 or bumpiness_delta < 0
       or height_delta < 0 or holes_delta < 0):
        scores_delta = 0
        previous_score = 0
        drops_delta = 0
        previous_drops = 0
        bumpiness_delta = 0
        previous_bumpiness = 0
        height_delta = 0
        previous_height = 0
        holes_delta = 0
        previous_holes = 0
    else:
        previous_score = game.get_score()
        previous_drops = game.get_drops()
        previous_bumpiness = game.get_bumpiness()
        previous_height = game.get_aggregate_height()
        previous_holes = game.get_number_holes()
    terms = [0.89*scores_delta, 0.01*drops_delta,
             0.034*bumpiness_delta,
             0.033*height_delta,
             0.033*holes_delta]
    return sum(terms)


def main() -> None:
    game = TetrisGame(60)
    renderer = Renderer(game)
    renderer.setup()
    agent = DQNAgent(210, 3)
    running = True
    game.step()
    renderer.rerender()
    current_state = game.get_simple_board().flatten()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        next_states = []
        for action in range(7):
            new_game = copy.deepcopy(game)
            new_game.set_next_input(action)
            new_game.step()
            next_states.append(new_game.get_simple_board().flatten())
            best_state = agent.select_state(next_states, magic=True)

            if game.is_over():
                agent.train(len(agent.memory))
                game.reset()
            else:
                print("The best state is, ", best_state)
                for i, state in enumerate(next_states):
                    if np.all(state == best_state):
                        best_action = i
                        break
                print("The best action is ", best_action)
                game.set_next_input(best_action)
                game.step()
                renderer.rerender()
                print(utility(game))
                agent.remember(current_state, best_state, utility(game),
                               game.is_over())
                current_state = best_state


if __name__ == '__main__':
    main()
