from game import Game
import math
import random
import numpy as np
import torch
from model import NeuralNetwork,QTrainer
import matplotlib.pyplot as plt
from IPython import display
from collections import deque

#tracking score between games
plt.ion()
def plot(scores, mean_scores):
    display.clear_output(wait=True)
    display.display(plt.gcf())
    plt.clf()
    plt.title('Training...')
    plt.xlabel('Number of Games')
    plt.ylabel('Score')
    plt.plot(scores)
    plt.plot(mean_scores)
    plt.ylim(ymin=0)
    plt.text(len(scores)-1, scores[-1], str(scores[-1]))
    plt.text(len(mean_scores)-1, mean_scores[-1], str(mean_scores[-1]))
    plt.show(block=False)
    plt.pause(.1)



# initials values
Snake = Game()
Snake.snakeSpeed=1000

moves = ['Straight','Left','Right']
directions = ['UP', 'LEFT', 'DOWN', 'RIGHT']


MAX_MEMORY = 100_000
BATCH_SIZE = 1000
memory = deque(maxlen=MAX_MEMORY) 

state=[]
plotScores = []
plotMeanScores = []
a = (Snake.fruitPosition[0]-Snake.snakePosition[0])/10
b = (Snake.fruitPosition[1]-Snake.snakePosition[1])/10
fruitDistance=math.sqrt(a ** 2 + b ** 2)
previousFruitDistance = fruitDistance

action= ""
agentAction=""

lr=0.001
discount = 0.9
model=NeuralNetwork()
iteration = 0
totalScore=0
record = 0
trainer = QTrainer(model,lr,discount)

#calc reward
def calc_reward():
    global fruitDistance,previousFruitDistance

    #snake has died
    if(Snake.death == True):

        return -10
    
    #snake has eaten the food
    if(Snake.eaten == True):
        Snake.eaten=False
        return 10
    #snake got closer to food
    if(previousFruitDistance>fruitDistance):
        return 1
    
    #snake got futher from food
    return -1


#Get state from game to agent
def get_state():
    global Snake

    fruitUp,fruitDown,fruitLeft,fruitRight = Snake.check_fruit()
    wallFront,wallLeft,wallRight = Snake.check_wall()
    snakeUp,snakeDown,snakeLeft,snakeRight = Snake.check_dir()
    return [snakeUp,snakeDown,snakeLeft,snakeRight,
            wallFront,wallLeft,wallRight,
            fruitUp,fruitDown,fruitLeft,fruitRight]

#Agent making decision
def get_action(epsilon,state,model):
    final_move = [0, 0, 0]
    #random action
    if random.randint(0, 100) < epsilon:
        move = random.randint(0, 2)
        final_move = moves[move]
    #from network
    else:
        state0 = torch.tensor(state, dtype=torch.float)
        prediction = model(state0)
        move = torch.argmax(prediction).item()
        final_move = moves[move]
    return final_move

#remeber current move
def remember(state, action, reward, next_state, done):
        global memory
        memory.append((state, action, reward, next_state, done))

#remeber current game
def train_long_memory(trainer):
        global memory
        if len(memory) > BATCH_SIZE:
            mini_sample = random.sample(memory, BATCH_SIZE)  # list of tuples
        else:
            mini_sample = memory

        states, actions, rewards, next_states, dones = zip(*mini_sample)
        trainer.train_step(states, actions, rewards, next_states, dones)

#train current move
def train_short_memory(trainer, state, action, reward, next_state, done):
        trainer.train_step(state, action, reward, next_state, done)

     
# Main Function ( Agent )
while True:
 
    # state of the game
    previousFruitDistance = fruitDistance
    state = get_state()

    # random actions
    epsilon = 80 - iteration
    choice = ""
    agentAction = get_action(epsilon,state,model)      
    temp = np.array(directions)

    # convert action to diretion and move in game
    if (agentAction == "Straight"):
        Snake.playStep(Snake.direction)
        action = [1,0,0]

    if (agentAction=="Left"):
        i = list(temp).index(Snake.direction)
        if (i!= 3):
            i+=1
            choice = directions[i]
        else:
            choice = directions[0]
        action = [0,1,0]    
        Snake.playStep(choice)

    if (agentAction=="Right"):
        i = list(temp).index(Snake.direction)
        if (i!= 0):
            i-=1
            choice = directions[i]
        else:
            choice = directions[3]
        action = [0,0,1]    
        Snake.playStep(choice)


    a = (Snake.fruitPosition[0]-Snake.snakePosition[0])/10
    b = (Snake.fruitPosition[1]-Snake.snakePosition[1])/10
    fruitDistance = math.sqrt(a ** 2 + b ** 2)
   
    # what happend after move in game
    reward = calc_reward()
    futureState = get_state()

    # train move based on reward and future state
    train_short_memory(trainer,state,action,reward,futureState,Snake.death)
    remember(state, action, reward, futureState,Snake.death)

    # remeber game after death
    if(Snake.death == True):
        train_long_memory(trainer)
        Snake.death = False
        if (record<Snake.score):
            record=Snake.score
            model.save()



        print('Game', iteration, 'Score', Snake.score, 'Record:', record)
        iteration += 1
        plotScores.append(Snake.score)
        totalScore += Snake.score
        mean_score = totalScore / iteration
        plotMeanScores.append(mean_score)
        Snake.reset_Game()
        plot(plotScores, plotMeanScores)


