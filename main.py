import time
import random
import pygame



class Snake:
    def __init__(self, starting_pos):
        self.snake_head = list(starting_pos)
        self.snake_body = [[]]
        self.current_direction = "RIGHT"
        self.create_snake(starting_pos)

    def create_snake(self, starting_pos):
        self.snake_body = [[starting_pos[0], starting_pos[1]],
                 [starting_pos[0] - 10, starting_pos[1]],
                 [starting_pos[0] - 20, starting_pos[1]],
                 [starting_pos[0] - 30, starting_pos[1]],
                 ]

    def draw(self):
        for position in self.snake_body:
            pygame.draw.rect(screen, pygame.Color(255, 255, 255), pygame.Rect(position[0], position[1], 10, 10))



    def valid_direction(self,direction):
        if direction == "UP" and self.current_direction != "DOWN":
            self.current_direction = "UP"
        if direction == "RIGHT" and self.current_direction != "LEFT":
            self.current_direction = "RIGHT"
        if direction == "DOWN" and self.current_direction != "UP":
            self.current_direction = "DOWN"
        if direction == "LEFT" and self.current_direction != "RIGHT":
            self.current_direction = "LEFT"

        else:
            self.current_direction = self.current_direction

    def movement(self):
        if self.current_direction == "UP":
            self.snake_head[1] -= 10
        if self.current_direction == "RIGHT":
            self.snake_head[0] += 10
        if self.current_direction == "DOWN":
            self.snake_head[1] += 10
        if self.current_direction == "LEFT":
            self.snake_head[0] -= 10

        self.snake_body.insert(0,list(self.snake_head))
        self.snake_body.pop()

    def extend(self):
        # Get the last segment of the snake's body
        last_segment = self.snake_body[-1]

        # Determine the direction in which the snake is moving and add a new segment accordingly
        if self.current_direction == "UP":
            new_segment = [last_segment[0], last_segment[1] + 10]
        elif self.current_direction == "RIGHT":
            new_segment = [last_segment[0] - 10, last_segment[1]]
        elif self.current_direction == "DOWN":
            new_segment = [last_segment[0], last_segment[1] - 10]
        elif self.current_direction == "LEFT":
            new_segment = [last_segment[0] + 10, last_segment[1]]

        # Append the new segment to the snake's body
        self.snake_body.append(new_segment)

class Fruit:
    def __init__(self, screen_rect):
        self.screen_rect = screen_rect
        self.fruit_position = []

    def set_position(self):
        self.fruit_position = [(random.uniform(self.screen_rect["x"],
                                               self.screen_rect["x"] + self.screen_rect["w"] - 10) // 10) * 10,
                               (random.uniform(self.screen_rect["y"],
                                               (self.screen_rect["y"] + self.screen_rect["h"] - 10)) // 10) * 10]

    def draw(self):
        print(self.fruit_position)
        pygame.draw.rect(screen, (0, 255, 0), pygame.Rect(
            self.fruit_position[0], self.fruit_position[1], 10, 10))

    # Return the current position of the fruit
    def get_position(self):
        return self.fruit_position

    # Check if the snake's head has collided with the fruit
    def check_collision(self, snake_head_position):
        return self.fruit_position == snake_head_position

    # Move the fruit to a new random position after it's eaten
    def respawn(self):
        self.set_position()


pygame.init()
snake_speed = 10

screen_x = 1000
screen_y = 1000

screen = pygame.display.set_mode((screen_x,screen_y))
screen.fill((0, 0, 0))

human_screen_rect_dict = {"x": screen_x/4, "y": screen_y/4, "w": 600, "h": 600}  # (x,y) refer to top left corner, (w,h) are width and height
human_screen_mid = (human_screen_rect_dict["x"]+human_screen_rect_dict["w"]/2,
                    human_screen_rect_dict["y"]+human_screen_rect_dict["h"]/2)  # calculates mid point for player snake spawn
human_game_screen = pygame.Rect(human_screen_rect_dict["x"], human_screen_rect_dict["y"],
                                human_screen_rect_dict["w"], human_screen_rect_dict["h"])


pygame.display.set_caption("Snake")
current_direction = "RIGHT"
direction = "RIGHT"
run = True
#snake = pygame.draw.rect(screen, pygame.Color(255,255,255), pygame.Rect(0,0,24,24), width=1)
fps = pygame.time.Clock()

# Snake position
snake = Snake(human_screen_mid)

# snake_head = [human_screen_mid[0], human_screen_mid[1]]
# snake = [  [human_screen_mid[0], human_screen_mid[1]],
#            [human_screen_mid[0] -10, human_screen_mid[1]],
#            [human_screen_mid[0] -20, human_screen_mid[1]],
#            [human_screen_mid[0] -30, human_screen_mid[1]],
#        ]

# fruit position
# fruit_position = [(random.uniform(human_screen_rect_dict["x"], human_screen_rect_dict["x"]+human_screen_rect_dict["w"]-10)//10)*10,
#                   (random.uniform(human_screen_rect_dict["y"], (human_screen_rect_dict["y"]+human_screen_rect_dict["h"]-10))//10)*10]
fruit = Fruit(human_screen_rect_dict)

fruit_spawn = True
score = 0
def game_over():
    time.sleep(5)
    screen.fill((255,0,0))
    pygame.display.update()
    time.sleep(2)

    return False


pygame.draw.rect(screen, pygame.Color(255, 0, 255), human_game_screen,width=1)
snake.draw()
pygame.display.update()

fruit.set_position()
while run:


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
    #print(snake.snake_body)
    snake.valid_direction(direction)
    snake.movement()

    if fruit.check_collision(snake.snake_head):
       snake.extend()
       fruit.respawn()

    screen.fill((0, 0, 0),human_game_screen)

    # draw snake
    snake.draw()
    # draw fruit
    fruit.draw()

    # draw human screen
    pygame.draw.rect(screen, pygame.Color(255, 0, 255), human_game_screen, width=1)


    if snake.snake_head[0] < human_screen_rect_dict["x"] or snake.snake_head[0] == human_screen_rect_dict["x"]+human_screen_rect_dict["w"]: # The conditional operators here are because the display updates act funny
        print(snake.snake_head)
        print(human_screen_rect_dict["x"],human_screen_rect_dict["y"])
        run =  game_over()
    if snake.snake_head[1] < human_screen_rect_dict["y"] or snake.snake_head[1] == human_screen_rect_dict["y"]+human_screen_rect_dict["h"]:
        run = game_over()

    for body in snake.snake_body[1:]:
        if snake.snake_head[0] == body[0] and snake.snake_head[1] == body[1]:
            game_over()
    pygame.display.update()
    fps.tick(snake_speed)
pygame.quit()