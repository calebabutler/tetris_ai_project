import random
import numpy as np
import tensorflow as tf
import time
import pygame
from collections import deque
from keras.models import Sequential, save_model, load_model
from keras.layers import Dense
from tetris_game import TetrisGame,Input
from renderer import Renderer




MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001

class DQNAgent:
    def __init__(self, state_size, action_size):
        self.state_size = state_size #The Number of State Information - Positon and Rotation as well as board statistics which gives 6
        self.action_size = action_size #Action Size are possible actions which will be rotate clockwise, move left, and move right

        self.memory = deque(maxlen=MAX_MEMORY) #Storing memories that can be replayed to train the Deep Q Network
        self.gamma = 0.95 # The discount factor that discounts prospective rewards in future steps
        self.epsilon = 1.0 # The factor that determins what portion of agents move are random
        self.epsilon_decay = 0.005 # Exploration rate that decays to allow agent to use info it learned
        self.epsilon_min = 0.01 # Minimmum for exploration rate given its 0.01 the agent only explores 1% of time and uses exp other 99%
        self.learning_rate = 0.001 #
        self.model = self._build_model()

    def _build_model(self):
        model = Sequential()
        model.add(Dense(32,activation="relu",input_dim=self.state_size))
        model.add(Dense(32,activation="relu"))
        model.add(Dense(self.action_size,activation="linear"))
        model.compile(loss="mse",optimizer=tf.keras.optimizers.Adam(lr=self.learning_rate))
        return model
    
    def remember(self, state, next_state, reward, done):
        self.memory.append((state, next_state, reward, done))

    def act(self, state):
        state = np.reshape(state,[1,self.state_size])
        if np.random.random() <= self.epsilon:
            return random.randrange(self.action_size)
        else:
            return np.argmax(self.model.predict(state))
    
    def predict_val(self,state):
        return self.model.predict(state)[0]
    
    def select_state(self, states, magic=False):
        max_value = None
 
        if random.random() <= self.epsilon:
            return random.choice(list(states))
        else:
            count = 0
            for state in states:
                temp_val_sum = 0
                temp_max_val_sum = 0
                if (count == 0):
                    val = self.predict_val(np.reshape(state,[1,self.state_size]))
                    print("The value is", val)
                    count = count + 1
                    max_val = val
                    best_state = state
                else:
                    val = self.predict_val(np.reshape(state,[1,self.state_size]))
                if magic:
                    for i in range(0,2): temp_val_sum = val[i] + val[i+1]
                    for i in range(0,2): temp_max_val_sum = max_val[i] + max_val[i+1]
                else:
                    for i in range(0,4): temp_val_sum = val[i] + val[i+1]
                    for i in range(0,4): temp_max_val_sum = max_val[i] + max_val[i+1]
                if (count > 0 and temp_val_sum > temp_max_val_sum):
                    max_val = val
                    best_state = state
        return best_state

    
    def train(self,batch_size):
        batch_sample = random.sample(self.memory, batch_size)
        next_states = np.array([x[1] for x in batch_sample])
        next_qs = [x[0] for x in self.model.predict(next_states)]
        x=[]
        y=[]
        
        for i,(state,__,reward,done) in enumerate(batch_sample):
            if (not done):
                new_q = reward + self.gamma * next_qs[i]
            else:
                new_q = reward
            x.append(state)
            y.append(new_q)
        
        self.model.fit(np.array(x),np.array(y),batch_size=batch_size,epochs=3,verbose=0)

        if self.epsilon > self.epsilon_min:
            self.epsilon -= self.epsilon_decay

def main() -> None:
    print("Hit loop")
    game = TetrisGame(60) 
    renderer = Renderer(game)
    renderer.setup()
    agent = DQNAgent(4,5)
    running = True
    scores = []
    game.step()
    renderer.rerender()
    current_state = game.get_board_statistics()
    steps = 0
    reset_code = False 
    reset_inner_loop_1 = False
    reset_inner_loop_2 = False
    while running:
        next_state = game.get_next_state()
        best_state = agent.select_state(next_state.values())
        best_action = None

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if(game.is_over()):
            reset_code = True
        
        if (reset_code == True):
            agent.train(len(agent.memory))
            game.reset()
            
        elif(reset_code == False):
            print("The best state is, ",best_state)
            for action, state in next_state.items():
                if state == best_state:
                    best_action = action
                    break
            print("The best action is ", best_action)

            while(game.get_current_piece().rotation != best_action[1]):
                game.set_next_input(Input.C_ROTATE.value)
                game.step()
                renderer.rerender()
                if(game.is_over()):
                    reset_inner_loop_1 = True
                    break
            if(reset_inner_loop_1 == False):
                while(game.get_current_piece().position[0] != best_action[0]):
                    if(best_action[0] < game.get_current_piece().position[0]):
                        game.set_next_input(Input.MOVE_LEFT.value)
                    else:
                        game.set_next_input(Input.MOVE_RIGHT.value)
                    game.step()
                    renderer.rerender()
                    if(game.is_over()):
                        reset_inner_loop_2 = True
                        break
            if(reset_inner_loop_1 == True or reset_inner_loop_2 == True):
                game.reset()
            if(reset_inner_loop_1 == False and reset_inner_loop_2 == False):
                game.set_next_input(Input.HARD_DROP.value)
                game.step()
                renderer.rerender()
                reward = game.get_score()
                done = game.is_over()
                if(not(done)):
                    agent.remember(current_state,next_state[best_action],reward,done)
                    current_state = next_state[best_action]
                    scores.append(game.get_score())
                    #steps += 1
                    #if(steps == 33):
                    #    steps = 0
                    #    
                    game.step()
                    renderer.rerender()
                    #time.sleep(1)
                    if(game.is_over()):
                        agent.train(len(agent.memory))
                        game.reset()
                else:
                    agent.train(len(agent.memory))
                    game.reset()
            reset_inner_loop_1 = False
            reset_inner_loop_2 = False
        reset_code = False

if __name__ == '__main__':
    main()




        



