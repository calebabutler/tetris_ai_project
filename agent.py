import torch
import random
import numpy as np
from collections import deque
from tetris_game import TetrisGame,Piece,Input

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001

class Agent:
    def __init__(self):
        self.number_games = 0
        self.epsilon = 0 # Parameter to control randomness
        self.gamma = 0 # Discount Rate
        self.memory = deque(maxlen=MAX_MEMORY) # Stack that keeps meory and pops out if full and push in new memory

    def get_state(self, game):
        return game.get_simple_board
    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE) # List of tuples
        else:
            mini_sample = self.memory
        
        for state,action,reward,next_state,done in mini_sample:
            self.trainer.train(state,action,reward,next_state,done)
            



    def train_short_memory(self, state, action, reward, next_state, done):
        self.trainer.train_step(state,action,reward, next_state, done)

    def get_action(self, state):
        self.epsilon = 100 - self.number_games
        final_move = [0,0,0]
        if random.randint(0, 200) < self.epsilon:
            move = random.randint(0, 2)
            final_move[move] = 1
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model.predict(state0)
            move = torch.argmax(prediction).item()
            final_move[move] = 1
            
        return final_move

def train():
    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    record = 0
    agent = Agent()
    game = TetrisGame(60)
    while True:
        # Get current state
        state_current = agent.get_state(game)

        # Get new move
        current_move = agent.get_action(state_current)

        # Execute the move and get new state after 
        reward, done, score = game.set_next_input(current_move)
        state_new = agent.get_state(game)

        # Train short memory
        agent.train_short_memory(state_current,current_move,reward,state_new,done)

        # Remember the
        agent.remember(state_current,current_move,reward,state_new,done)

        if done:
            # Store in long memory, plot result
            ##game.is_game_over
            agent.number_games += 1
            agent.train_long_memory()

            if score > record:
                record = score
                #agent.model.save()
            print('Game', agent.number_games,'Score',score,'Rercord: ',record)
            #PLOT
            game = game
        
             

if __name__ == '__main__':
    train() 