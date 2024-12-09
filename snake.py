# importing libraries
import pygame
import time
import random

# colors
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)

# initials values

window_x = 720
window_y = 480


snake_speed = 15
snake_position = [100, 50]
snake_body = [[100, 50],
              [90, 50],
              [80, 50],
              [70, 50]]
direction = 'RIGHT'
change_to = direction

fruit_position = [random.randrange(20, (window_x//10)-3) * 10, 
                    random.randrange(20, (window_y//10)-3) * 10]

fruit_position = [20,20]
fruit_spawn = True
score = 0

walls = pygame.Rect(10, 10, 710, 470)

active_agent = True


# pygame initialization
pygame.init()
pygame.display.set_caption('Wonsz Rzeczny')
game_window = pygame.display.set_mode((window_x, window_y))
fps = pygame.time.Clock()

moves = ['UP', "DOWN", 'LEFT', 'RIGHT']

# function for reseting game
def reset_game():  

    global fruit_position
    global snake_position
    global snake_body
    global direction
    global change_to
    global score

    fruit_position = [random.randrange(1, (window_x//10)) * 10, 
                  random.randrange(1, (window_y//10)) * 10]
    snake_position = [100, 50]


    snake_body.clear()
    snake_body = [[100, 50],
                [90, 50],
                [80, 50],
                [70, 50]
                ]

    direction = 'RIGHT'
    change_to = direction

    score = 0
    pygame.display.update()

# drawing score and exit info
def draw_gui(color, font, size):
  
    font = pygame.font.SysFont(font, size)

    score_surface = font.render('Score : ' + str(score), True, color)
    score_rect = score_surface.get_rect()
    score_rect.midbottom = (window_x/2, 20)
    game_window.blit(score_surface, score_rect)

    exit_surface = font.render('Esc to exit', True, color)
    exit_rect = score_surface.get_rect()
    exit_rect.midleft = (20, 10)
    game_window.blit(exit_surface, exit_rect)


# game over function
def game_over():
  

    my_font = pygame.font.SysFont('times new roman', 50)
    
    game_over_surface = my_font.render('Your Score is : ' + str(score), True, red)
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.midtop = (window_x/2, window_y/4)

    info_text = my_font.render('press n to reset game, esc to exit', True, white)
    info_text_rect = info_text.get_rect()
    info_text_rect.midtop = (window_x/2, window_y/4+50)
    
    game_window.blit(game_over_surface, game_over_rect)
    game_window.blit(info_text , info_text_rect)
    pygame.display.flip()

    # User input 
    loop = True
    while loop:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_n:
                    reset_game()
                    loop = False
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()



# Main Function
while True:
    


    # User input 
    if (active_agent == False):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    change_to = 'UP'
                if event.key == pygame.K_DOWN:
                    change_to = 'DOWN'
                if event.key == pygame.K_LEFT:
                    change_to = 'LEFT'
                if event.key == pygame.K_RIGHT:
                    change_to = 'RIGHT'
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()

    # Agent manipulation
    if (active_agent == True):
        choice = moves[random.randrange(4)]

        change_to = choice

    # 2 keys at the same time
    if change_to == 'UP' and direction != 'DOWN':
        direction = 'UP'
    if change_to == 'DOWN' and direction != 'UP':
        direction = 'DOWN'
    if change_to == 'LEFT' and direction != 'RIGHT':
        direction = 'LEFT'
    if change_to == 'RIGHT' and direction != 'LEFT':
        direction = 'RIGHT'

    # Moving the snake
    if direction == 'UP':
        snake_position[1] -= 10
    if direction == 'DOWN':
        snake_position[1] += 10
    if direction == 'LEFT':
        snake_position[0] -= 10
    if direction == 'RIGHT':
        snake_position[0] += 10

    # Snake body growing
    snake_body.insert(0, list(snake_position))
    if snake_position[0] == fruit_position[0] and snake_position[1] == fruit_position[1]:
        score += 1
        fruit_spawn = False
    else:
        snake_body.pop()
    
    # Spawn fruit    
    if not fruit_spawn:
        loop = True
        while loop:
            fruit_position = [random.randrange(20, (window_x//10)-3) * 10, 
                            random.randrange(20, (window_y//10)-3) * 10]
            loop = False
            for poz in snake_body:
                if (poz[0] == fruit_position[0] and poz[1] == fruit_position[1]):
                    loop = True
                    break 
        
    fruit_spawn = True
    game_window.fill(black)
    
    # Draw walls
    pygame.draw.rect(game_window, blue,  pygame.Rect(20, 20, 680, 440),2)

    # Draw fruit
    pygame.draw.rect(game_window, white, pygame.Rect(fruit_position[0], fruit_position[1], 10, 10))
    # Draw snake
    for pos in snake_body:
        if (snake_body[0][0] == pos[0] and snake_body[0][1] == pos[1]):
            pygame.draw.rect(game_window, green, pygame.Rect(pos[0], pos[1], 10, 10))
        else:
            pygame.draw.rect(game_window, green, pygame.Rect(pos[0]+1, pos[1]+1, 8, 8))



    # Game Over conditions
    # Wall
    if snake_position[0] < 20 or snake_position[0] > window_x-30:
        game_over()
    if snake_position[1] < 20 or snake_position[1] > window_y-30:
        game_over()

    # Snake body
    for block in snake_body[1:]:
        if snake_position[0] == block[0] and snake_position[1] == block[1]:
            game_over()

    
    draw_gui( white, 'times new roman', 20)
    pygame.display.update()

    fps.tick(snake_speed)