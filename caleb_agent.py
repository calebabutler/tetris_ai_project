from tetris_game import TetrisGame
from renderer import Renderer
from agent import DQNAgent
import numpy as np
import copy


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
        next_states = []
        for action in range(7):
            new_game = copy.deepcopy(game)
            new_game.set_next_input(action)
            new_game.step()
            next_states.append(new_game.get_simple_board().flatten())
            best_state = agent.select_state(next_states)

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
                agent.remember(current_state, best_state, game.get_score(),
                               game.is_over())
                current_state = best_state


if __name__ == '__main__':
    main()
