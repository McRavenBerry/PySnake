import pygame, sys, random
from pygame.math import Vector2

# Adds title to the window
pygame.display.set_caption("PySnake")

class SNAKE:
    def __init__(self):
        self.body = [Vector2(7, 10), Vector2(6, 10), Vector2(5, 10)]
        self.direction = Vector2(1, 0)
        self.new_block = False

    def draw_snake(self):
        for block in self.body:
            # create a rect
            x_pos = int(block.x * cell_size)
            y_pos = int(block.y * cell_size)
            block_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)  # x, y, w, h
            # draw the rectangle
            pygame.draw.rect(screen, (61, 93, 224), block_rect)

    def move_snake(self):
        # Only allows us to move in a direction away from the body
        if self.body[0] + self.direction != self.body[1]:
            if self.new_block == True:
                body_copy = self.body
                body_copy.insert(0, body_copy[0] + self.direction)
                self.body = body_copy
                self.new_block = False
            else:
                body_copy = self.body[:-1]
                body_copy.insert(0, body_copy[0] + self.direction)
                self.body = body_copy
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0, body_copy[0] - self.direction)
            self.body = body_copy

    def add_block(self):
        self.new_block = True

    def reset(self):
        self.score = 0
        self.body = [Vector2(7, 10), Vector2(6, 10), Vector2(5, 10)]
        self.direction = Vector2(1, 0)


class FRUIT:
    # create an x and y position
    def __init__(self):
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(0, cell_number - 1)
        self.pos = Vector2(self.x, self.y)  # x, y

    # draw a square
    def draw_fruit(self):
        # create a rectangle
        x_pos = int(self.pos.x * cell_size)
        y_pos = int(self.pos.y * cell_size)
        fruit_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)  # x, y, w, h
        # draw the rectangle
        # surface, color, rectangle
        pygame.draw.rect(screen, (252, 3, 61), fruit_rect)

    def randomize(self):
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(0, cell_number - 1)
        self.pos = Vector2(self.x, self.y)


class MAIN:
    def __init__(self):
        self.fruit = FRUIT()
        self.snake = SNAKE()
        self.score = 0
        self.high_score = 0
        print("Welcome to PySnake!")

    def update(self):
        self.snake.move_snake()
        self.check_collision()
        self.check_fail()

    def draw_elements(self):
        self.fruit.draw_fruit()
        self.snake.draw_snake()
        self.draw_score()

    def check_collision(self):
        # check if the snake's head overlaps the fruit
        if self.fruit.pos == self.snake.body[0]:
            # move the fruit
            self.fruit.randomize()
            # add one block to the snake
            self.snake.add_block()
            self.score += 1
            if self.score > self.high_score:
                self.high_score = self.score
            print("Score: " + str(self.score))

        for block in self.snake.body[1:]:
            if block == self.fruit.pos:
                self.fruit.randomize()

    # game over
    def check_fail(self):
        # moves off screen, game over
        if not 0 <= self.snake.body[0].x < cell_number or not 0 <= self.snake.body[0].y < cell_number:
            self.game_over()
        # runs into self, game over
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()

    # calls to reset the game
    def game_over(self):
        print("Game Over!")
        print(f"High Score: {self.high_score}")
        self.snake.reset()
        self.score = 0

    # Add score to the screen
    def draw_score(self):
        self.font_color = (0,0,0)
        self.game_font = pygame.font.Font("font/Computerfont.ttf",25)
        self.score_text = self.game_font.render("Score: " + str(self.score) + 
            "     High Score: " + str(self.high_score), True, self.font_color)
        self.text_rect = self.score_text.get_rect(center=(screen.get_width()/2, 15))
        screen.blit(self.score_text, self.text_rect)

pygame.init()
cell_size = 20
cell_number = 20
screen = pygame.display.set_mode((cell_number * cell_size, cell_number * cell_size))  # width, height
clock = pygame.time.Clock()

main_game = MAIN()

# Timer
SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)

while True:
    # draw all our elements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == SCREEN_UPDATE:
            main_game.update()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                main_game.snake.direction = Vector2(0, -1)
            if event.key == pygame.K_DOWN:
                main_game.snake.direction = Vector2(0, 1)
            if event.key == pygame.K_LEFT:
                main_game.snake.direction = Vector2(-1, 0)
            if event.key == pygame.K_RIGHT:
                main_game.snake.direction = Vector2(1, 0)

    screen.fill((175, 215, 70))
    main_game.draw_elements()
    pygame.display.update()
    clock.tick(60)  # framerate: 60 frames per second