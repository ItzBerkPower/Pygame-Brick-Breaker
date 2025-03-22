import random
import pygame
from models.brick import Brick
from constants import *

def generate_bricks(level):
    bricks = []
    rows = 3 + level
    for row in range(rows):
        for col in range(SCREEN_WIDTH // brick_width):
            brick = Brick(col * brick_width, row * brick_height, brick_width, brick_height)
            bricks.append(brick)
    return bricks

def update_game_objects(paddle, balls, keys):
    paddle.move(keys)
    for ball in balls:
        ball.move()

def event_handling():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
    return True