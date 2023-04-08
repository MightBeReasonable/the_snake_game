from typing import SupportsFloat
import pygame
import sys
import random
import time

from pygame.constants import K_x, K_z

pygame.init()
# Set caption and logo
pygame.display.set_caption("The Snake Game")
icon = pygame.image.load("snake.png")
pygame.display.set_icon(icon)

pygame.mixer.pre_init(44100, -16, 2, 64)

class Snake(object):
    def __init__(self):
        self.length = 1
        self.positions = [((SCREEN_WIDTH/2), (SCREEN_HEIGHT/2))]
        self.direction = RIGHT
        self.color = (0, 204, 0)

    def get_head_position(self):
        return self.positions[0]

    def turn(self, point):
        if self.length > 1 and (point[0]*-1, point[1]*-1) == self.direction:
            return
        else:
            self.direction = point
    
    def move(self):
        cur = self.get_head_position()
        x, y = self.direction
        new = (((cur[0]+x*GRID_SIZE) % SCREEN_WIDTH), ((cur[1]+y*GRID_SIZE) % SCREEN_HEIGHT))

        self.positions.insert(0, new)

        if len(self.positions) > self.length:
            self.last_position = self.positions.pop()

        return new

    def reset(self):
        pygame.mixer.music.play(-1)
        self.length = 1
        self.positions = [((SCREEN_WIDTH/2), (SCREEN_HEIGHT/2))]
        self.direction = RIGHT


    def draw(self, surface):
        for p in self.positions:
            r = pygame.Rect((p[0], p[1]), (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, self.color, r)
            pygame.draw.rect(surface, (0, 0, 0), r, 1)

        r = pygame.Rect((self.last_position[0], self.last_position[1]), (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, (0, 0, 0), r)

    def handle_keys(self):
        events = pygame.event.get()
        if len(events) == 0:
            return
        elif len(events) != 0:
            event = events[-1]
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.turn(UP)
                elif event.key == pygame.K_DOWN:
                    self.turn(DOWN)
                elif event.key == pygame.K_LEFT:
                    self.turn(LEFT)
                elif event.key == pygame.K_RIGHT:
                    self.turn(RIGHT)
                elif event.key == pygame.K_ESCAPE:
                    global playing
                    playing = False
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_q:
                    pygame.mixer.music.fadeout(1000)
                if event.key == pygame.K_w:
                    pygame.mixer.music.play(-1)

class Food(object):
    def __init__(self, snake_positions):
        self.position = (0, 0)
        self.color = (255, 0, 0)
        self.randomize_position(snake_positions)

    def randomize_position(self, snake_positions):
        tuple_position = self.generate_random_position(snake_positions)
        self.position = tuple_position

    def generate_random_position(self, snake_positions):
        x_position = random.randint(0, GRID_WIDTH-1)*GRID_SIZE
        y_position = random.randint(0, GRID_HEIGHT-1)*GRID_SIZE
        return (x_position, y_position) if (x_position, y_position) not in snake_positions else self.generate_random_position(snake_positions)
        
    def draw(self, surface):
        r = pygame.Rect((self.position[0], self.position[1]), (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.color, r)
        pygame.draw.rect(surface, (0, 0, 0), r, 1)

def drawGrid(surface):
    for y in range(0, int(GRID_HEIGHT)):
        for x in range(0, int(GRID_WIDTH)):
            if (x + y) % 2 == 0:
                r = pygame.Rect((x*GRID_SIZE, y*GRID_SIZE), (GRID_SIZE, GRID_SIZE))
                pygame.draw.rect(surface, (0, 0, 0), r, -1)

def set_screen_and_surface(SCREEN_WIDTH, SCREEN_HEIGHT):
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
    surface = pygame.Surface(screen.get_size())
    surface = surface.convert()
    drawGrid(surface)
    return screen, surface

SCREEN_WIDTH = 480
SCREEN_HEIGHT = 480

GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH/GRID_SIZE
GRID_HEIGHT = SCREEN_WIDTH/GRID_SIZE

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

bite_sound = pygame.mixer.Sound('.\sounds\\bite.wav')
bite_sound.set_volume(0.2)
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.load('.\sounds\sonata_piano_loop.mp3')

def game():
    global playing
    playing = True
    pygame.mixer.music.play(-1)

    clock = pygame.time.Clock()
    screen, surface = set_screen_and_surface(SCREEN_WIDTH, SCREEN_HEIGHT)
    
    snake = Snake()
    food = Food(snake.positions)

    myfont = pygame.font.SysFont("monospace", 16)

    score = 0

    while playing:
        clock.tick(12)
        drawGrid(surface)
        
        new_head_position = snake.move()
        
        if len(snake.positions) > 2 and new_head_position in snake.positions[4:]:
            pygame.mixer.music.fadeout(1000)
            pygame.time.wait(5000)
            snake.reset()
            screen, surface = set_screen_and_surface(SCREEN_WIDTH, SCREEN_HEIGHT)
            drawGrid(surface)

            score = 0

        if snake.get_head_position() == food.position:
            bite_sound.play()
            snake.length += 1
            score += 1
            food.randomize_position(snake.positions)
        
        snake.handle_keys()
        snake.draw(surface)
        food.draw(surface)
        
        screen.blit(surface, (0, 0))
        text = myfont.render("Score {0}".format(score), 1, (255, 255, 255))
        screen.blit(text, (5, 10))

        pygame.display.update()
        if playing == False:
            return playing
