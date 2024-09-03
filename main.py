import time
import random
import pygame
import pygame.examples







class Snake:
    def __init__(self, starting_pos):
        starting_pos = starting_pos


pygame.init()
snake_speed = 10




screen_x = 1000
screen_y = 1000

screen = pygame.display.set_mode((screen_x,screen_y))
screen.fill((0, 0, 0))
human_screen_rect_dict = {"x":screen_x/4, "y":screen_y/4, "w":600, "h":600} # (x,y) refer to top left corner, (w,h) are width and height
human_screen_mid = (human_screen_rect_dict["x"]+human_screen_rect_dict["w"]/2, human_screen_rect_dict["y"]+human_screen_rect_dict["h"]/2) # calculates mid point for player snake spawn
human_game_screen = pygame.Rect(human_screen_rect_dict["x"],human_screen_rect_dict["y"],human_screen_rect_dict["w"],human_screen_rect_dict["h"]) # could make this a dict


pygame.display.set_caption("Snake")
current_direction = "RIGHT"
direction = "RIGHT"
run = True
#snake = pygame.draw.rect(screen, pygame.Color(255,255,255), pygame.Rect(0,0,24,24), width=1)
fps = pygame.time.Clock()

# Snake position
snake_head = [human_screen_mid[0], human_screen_mid[1]]
snake = [  [human_screen_mid[0], human_screen_mid[1]],
           [human_screen_mid[0] -10, human_screen_mid[1]],
           [human_screen_mid[0] -20, human_screen_mid[1]],
           [human_screen_mid[0] -30, human_screen_mid[1]],
       ]

# fruit position
fruit_position = [(random.uniform(human_screen_rect_dict["x"], human_screen_rect_dict["x"]+human_screen_rect_dict["w"]-10)//10)*10,
                  (random.uniform(human_screen_rect_dict["y"], (human_screen_rect_dict["y"]+human_screen_rect_dict["h"]-10))//10)*10]


fruit_spawn = True
score = 0
def game_over():
    time.sleep(5)
    screen.fill((255,0,0))
    pygame.display.update()
    time.sleep(2)

    return False
def movement(direction, current_direction,snake_head):
    if direction == "UP" and current_direction != "DOWN":
        current_direction = "UP"
    if direction == "RIGHT" and current_direction != "LEFT":
        current_direction = "RIGHT"
    if direction == "DOWN" and current_direction != "UP":
        current_direction = "DOWN"
    if direction == "LEFT" and current_direction != "RIGHT":
        current_direction = "LEFT"

    if current_direction == "UP":
        snake_head[1] -= 10
    if current_direction == "RIGHT":
        snake_head[0] += 10
    if current_direction == "DOWN":
        snake_head[1] += 10
    if current_direction == "LEFT":
        snake_head[0] -= 10

    return current_direction, snake_head
print("fruit", fruit_position)
pygame.draw.rect(screen, pygame.Color(255, 0, 255), human_game_screen,width=1)
pygame.display.update()
while run:
   # print(snake_head)

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                direction = "UP"
            if event.key == pygame.K_DOWN:
                direction = "DOWN"
            if event.key == pygame.K_RIGHT:
                direction = "RIGHT"
            if event.key == pygame.K_LEFT:
                direction = "LEFT"


    snake.insert(0, list(snake_head))
    if snake_head[0] == fruit_position[0] and snake_head[1] == fruit_position[1]:
        score += 10
        fruit_spawn = False
    else:
        snake.pop()

    current_direction, snake_head = movement(direction, current_direction, snake_head)

    if not fruit_spawn:
        fruit_position = [int(random.uniform(human_screen_rect_dict["x"],
                                            human_screen_rect_dict["x"] + human_screen_rect_dict["w"] - 10) // 10) * 10,
                          int(random.uniform(human_screen_rect_dict["y"], (
                                      human_screen_rect_dict["y"] + human_screen_rect_dict["h"] - 10)) // 10) * 10]

    fruit_spawn = True
    screen.fill((0, 0, 0),human_game_screen)
    # draw snake
    for position in snake:
        pygame.draw.rect(screen, pygame.Color(255, 255, 255), pygame.Rect(position[0],position[1],10,10))
    # draw fruit
    pygame.draw.rect(screen, (0,255,0), pygame.Rect(
        fruit_position[0], fruit_position[1], 10, 10))
    # draw human screen
    pygame.draw.rect(screen, pygame.Color(255, 0, 255), human_game_screen, width=1)
    pygame.display.update()
    fps.tick(snake_speed)

    if snake_head[0] < human_screen_rect_dict["x"] or snake_head[0] == human_screen_rect_dict["x"]+human_screen_rect_dict["w"]: # The conditional operators here are because the display updates act funny
        print(snake_head)
        print(human_screen_rect_dict["x"],human_screen_rect_dict["y"])
        run =  game_over()
    if snake_head[1] < human_screen_rect_dict["y"] or snake_head[1] == human_screen_rect_dict["y"]+human_screen_rect_dict["h"]:
        run = game_over()

    for body in snake[1:]:
        if snake_head[0] == body[0] and snake_head[1] == body[1]:
            game_over()

pygame.quit()