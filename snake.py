from game import Game
import math
import random
import numpy as np

Snake = Game()
Snake.snakeSpeed=1000
# initials values
history = []

moves = ['Straight','Right','Left']
directions = ['UP', 'LEFT', 'DOWN', 'RIGHT']


state=[]


qValue=0
qTable=[]
iteretion = 0


#calc reward
def calc_reward():
    global fruitDistance,previousFruitDistance

    if(Snake.death == True):
        Snake.death = False
        return -10

    if(previousFruitDistance>fruitDistance):
        return 1
    
    return -1

a = (Snake.fruitPosition[0]-Snake.snakePosition[0])/10
b = (Snake.fruitPosition[1]-Snake.snakePosition[1])/10
fruitDistance=math.sqrt(a ** 2 + b ** 2)
#fruitDistance = pygame.math.Vector2(snakePosition[0], snakePosition[1]).distance_to((fruitPosition[0], fruitPosition[1]))
previousFruitDistance = fruitDistance

action= ""
agentAction=""

def get_state():
    global Snake

    fruitUp,fruitDown,fruitLeft,fruitRight = Snake.check_fruit()
    wallFront,wallLeft,wallRight = Snake.check_wall()
    snakeUp,snakeDown,snakeLeft,snakeRight = Snake.check_dir()
    return [snakeUp,snakeDown,snakeLeft,snakeRight,
            wallFront,wallLeft,wallRight,
            fruitUp,fruitDown,fruitLeft,fruitRight]

# Main Function
while True:
    
    # state of the game
    state = get_state()
    previousFruitDistance = fruitDistance
    
    # Agent 
    highestvalue = -10
    choice = ""

    # if beta > gamma take random action
    gamma = 10
    beta = random.randint(1, 100)
    agentAction = ""
    decisions=[]
    i = 0
    if(beta>gamma):
        for q in qTable:
            if(np.all(q[1] == state) == True):
                decisions.append(qTable[i])
                if(highestvalue<q[0]):
                    highestvalue = q[0]
                    agentAction = q[2]
        if (agentAction == ""):
            agentAction = moves[random.randrange(3)] 
        i+=1

    else:
        agentAction = moves[random.randrange(3)]
        #gamma = 10-0.01 
        
    temp = np.array(directions)

    if (agentAction == "Straight"):
        Snake.playStep(Snake.direction)

    if (agentAction=="Left"):
        i = list(temp).index(Snake.direction)
        if (i!= 3):
            i+=1
            choice = directions[i]
        else:
            choice = directions[0]
        Snake.playStep(choice)

    if (agentAction=="Right"):
        i = list(temp).index(Snake.direction)
        if (i!= 0):
            i-=1
            choice = directions[i]
        else:
            choice = directions[3]
        Snake.playStep(choice)

    action = agentAction

    a = (Snake.fruitPosition[0]-Snake.snakePosition[0])/10
    b = (Snake.fruitPosition[1]-Snake.snakePosition[1])/10
    fruitDistance = math.sqrt(a ** 2 + b ** 2)
    #fruitDistance = pygame.math.Vector2(snakePosition[0], snakePosition[1]).distance_to((fruitPosition[0], fruitPosition[1]))
   
    
    reward = calc_reward()
    history.append([state,action])

    
    i = 0
    new = True
    for q in qTable:
        #update a existing value in qtable
        if (np.all(q[1] == state) == True and q[2] == action):
            
            qTable[i][0] = max(q[0],reward)
            new = False
            break
        i+=1
    #add a new value do qtable
    if (new == True):
        qTable.append([reward,state,action])



