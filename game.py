import pygame
import random


class Game:
    # colors
    black = pygame.Color(0, 0, 0)
    white = pygame.Color(255, 255, 255)
    red = pygame.Color(255, 0, 0)
    green = pygame.Color(0, 255, 0)
    blue = pygame.Color(0, 0, 255)

    # Game 
    # one position is 10 by 10 pixels 
    window_x = 720
    window_y = 480
    gameWindow = ""

    walls = pygame.Rect(20, 20, 680, 440)
    # 2 * 10 = 20
    wallOffSet = 2

    score = 0
    fps = 0
    death = False
    eaten = False

    #snake
    snakePosition = [100, 50]
    snakeBody = [[100, 50],
              [90, 50],
              [80, 50],
              [70, 50]]
    snakeSpeed = 10

    direction = 'RIGHT'
    changeTo = direction

    #fruit
    fruitPosition = [random.randrange(wallOffSet, (window_x//10)-3) * 10, 
                    random.randrange(wallOffSet, (window_y//10)-3) * 10]
    
    fruitSpawn = True
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Wonsz Rzeczny')
        self.gameWindow = pygame.display.set_mode((self.window_x, self.window_y))
        self.fps = pygame.time.Clock()

    def reset_Game(self):  
        self.fruitPosition = [random.randrange(self.wallOffSet , (self.window_x//10)-3) * 10, #x
                               random.randrange(self.wallOffSet , (self.window_y//10)-3) * 10] #y
        self.snakePosition = [100, 50]


        self.snakeBody.clear()
        self.snakeBody = [[100, 50],
                    [90, 50],
                    [80, 50],
                    [70, 50]
                    ]
        self.direction = 'RIGHT'
        self.changeTo = self.direction
        self.score = 0
        pygame.display.update()

    # drawing score and exit info
    def draw_gui(self):
    
        font = pygame.font.SysFont('times new roman', 20)

        #draw score
        score_surface = font.render('Score : ' + str(self.score), True, self.white)
        score_rect = score_surface.get_rect()
        score_rect.midbottom = (self.window_x/2, 20)
        self.gameWindow.blit(score_surface, score_rect)

        #draw exit info
        exit_surface = font.render('Esc to exit', True, self.white)
        exit_rect = score_surface.get_rect()
        exit_rect.midleft = (20, 10)
        self.gameWindow.blit(exit_surface, exit_rect)

    # Game over function
    def Game_over(self):
        self.death = True

        # my_font = pygame.font.SysFont('times new roman', 50)
        
        # Game_over_surface = my_font.render('Your Score is : ' + str(self.score), True, self.red)
        # Game_over_rect = Game_over_surface.get_rect()
        # Game_over_rect.midtop = (self.window_x/2, self.window_y/4)

        # info_text = my_font.render('press n to reset Game, esc to exit', True, self.white)
        # info_text_rect = info_text.get_rect()
        # info_text_rect.midtop = (self.window_x/2, self.window_y/4+50)
        
        # self.gameWindow.blit(Game_over_surface, Game_over_rect)
        # self.gameWindow.blit(info_text , info_text_rect)
        # pygame.display.flip()



    # Moving the snake
    def snake_move(self):
        # 2 keys at the same time
        if self.changeTo == 'UP' and self.direction != 'DOWN':
            self.direction = 'UP'
        if self.changeTo == 'DOWN' and self.direction != 'UP':
            self.direction = 'DOWN'
        if self.changeTo == 'LEFT' and self.direction != 'RIGHT':
            self.direction = 'LEFT'
        if self.changeTo == 'RIGHT' and self.direction != 'LEFT':
            self.direction = 'RIGHT'

        #move    
        if self.direction == 'UP':
            self.snakePosition[1] -= 10
        if self.direction == 'DOWN':
            self.snakePosition[1] += 10
        if self.direction == 'LEFT':
            self.snakePosition[0] -= 10
        if self.direction == 'RIGHT':
            self.snakePosition[0] += 10

        
    # Snake body growing
    def snake_grow(self):
        self.snakeBody.insert(0, list(self.snakePosition))
        if self.snakePosition[0] == self.fruitPosition[0] and self.snakePosition[1] == self.fruitPosition[1]:
            self.score += 1
            self.eaten = True
            self.fruitSpawn = False
        else:
            self.snakeBody.pop()

    # Spawn fruit    
    def spawn_fruit(self):
        if not self.fruitSpawn:
            loop = True
            while loop:
                self.fruitPosition = [random.randrange(2, (self.window_x//10)-3) * 10, 
                                random.randrange(2, (self.window_y//10)-3) * 10]
                loop = False
                for poz in self.snakeBody:
                    if (poz[0] == self.fruitPosition[0] and poz[1] == self.fruitPosition[1]):
                        loop = True
                        break 
        self.fruitSpawn=True

    def draw(self):
        # Draw walls
        pygame.draw.rect(self.gameWindow, self.blue,  self.walls, 2)

        # Draw fruit
        pygame.draw.rect(self.gameWindow, self.white, pygame.Rect(self.fruitPosition[0], self.fruitPosition[1], 10, 10))
        
        # Draw snake
        for pos in self.snakeBody:
            if (self.snakeBody[0][0] == pos[0] and self.snakeBody[0][1] == pos[1]):
                pygame.draw.rect(self.gameWindow, self.green, pygame.Rect(pos[0], pos[1], 10, 10))
            else:
                pygame.draw.rect(self.gameWindow, self.green, pygame.Rect(pos[0]+1, pos[1]+1, 8, 8))
    
    # Game Over conditions
    def check_dead(self):
        # Hit Wall
        if self.snakePosition[0] < 20 or self.snakePosition[0] > self.window_x-30:
            self.Game_over()
        if self.snakePosition[1] < 20 or self.snakePosition[1] > self.window_y-30:
            self.Game_over()
            


        # Hit selfs
        for block in self.snakeBody[1:]:
            if self.snakePosition[0] == block[0] and self.snakePosition[1] == block[1]:
                self.Game_over()

    # Information for agent
    #
    #
    # where is fruit relative to snake
    def check_fruit(self):
        horizontal=self.snakePosition[0]-self.fruitPosition[0]
        vertical=self.snakePosition[1]-self.fruitPosition[1]

        fruitUp=False
        fruitDown=False
        fruitRight=False
        fruitLeft=False

        if(horizontal > 0):
            fruitLeft = True
        if(horizontal < 0):
            fruitRight = True
        if(vertical > 0):
            fruitUp = True
        if(vertical < 0):
            fruitDown = True

        return fruitUp,fruitDown,fruitLeft,fruitRight
    
    #check if wall or snake body is one position above
    def check_up(self):
        if (self.snakePosition[1]-10 < 20):
            return True    
        for b in self.snakeBody:
            if (self.snakePosition[1]-10 == b[1] and self.snakePosition[0] == b[0]):
                return True
        return False

    #check if wall or snake body is one position below
    def check_down(self):
        if (self.snakePosition[1]+10 >= self.window_y-20):
            return True
        for b in self.snakeBody:
            if (self.snakePosition[1]+10 == b[1] and self.snakePosition[0] == b[0]):
                return True
        return False  
            
    #check if wall or snake body is one position to the left
    def check_left(self):
        if (self.snakePosition[0]-10 < 20):
            return True
        for b in self.snakeBody:
            if (self.snakePosition[0]-10 == b[0] and self.snakePosition[1] == b[1]):
                return True 
        return False 

    #check if wall or snake body is one position to the right
    def check_right(self):
        if (self.snakePosition[0]+10 >= self.window_x-20):
            return True 
        for b in self.snakeBody:
            if (self.snakePosition[0]+10 == b[0] and self.snakePosition[1] == b[1]):
                return True
        return False  

    #check if snake has walls near him
    def check_wall(self):
        if(self.direction == 'UP'):

            wallFront = self.check_up()
            wallLeft = self.check_left()
            wallRight = self.check_right()

        if(self.direction == 'DOWN'):

            wallFront = self.check_down()
            wallLeft = self.check_right()
            wallRight = self.check_left()

        if(self.direction == 'RIGHT'):

            wallFront = self.check_right()
            wallLeft = self.check_up()
            wallRight = self.check_down()

        if(self.direction == 'LEFT'):
            
            wallFront = self.check_left()
            wallLeft = self.check_down()
            wallRight = self.check_up()
        
        return wallFront,wallLeft,wallRight
    
    #get snake movement direction
    def check_dir(self):
        snakeUp=False
        snakeDown=False
        snakeLeft=False
        snakeRight=False

        if(self.direction == 'UP'):
            snakeUp=True

        if(self.direction == 'DOWN'):
            snakeDown=True

        if(self.direction == 'RIGHT'):
            snakeRight=True

        if(self.direction == 'LEFT'):
            snakeLeft=True

        return snakeUp,snakeDown,snakeLeft,snakeRight
    
    def playStep(self,action = ""):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        #User input
        if (action == ""):
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.changeTo = 'UP'
                    if event.key == pygame.K_DOWN:
                        self.changeTo = 'DOWN'
                    if event.key == pygame.K_LEFT:
                        self.changeTo = 'LEFT'
                    if event.key == pygame.K_RIGHT:
                        self.changeTo = 'RIGHT'
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        quit()
        else:
            self.changeTo=action
        self.snake_move()
        self.snake_grow()
        self.spawn_fruit()
        self.gameWindow.fill(self.black)
        self.draw()
        self.check_dead()
        self.draw_gui()
        pygame.display.update()
        self.fps.tick(self.snakeSpeed)
        pygame.event.get()


        