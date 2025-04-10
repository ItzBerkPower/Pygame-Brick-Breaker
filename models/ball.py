# models/ball.py - Ball Class

import pygame
import random
from constants import *
from models.game_object import GameObject

class Ball(GameObject):
    # Initialising Ball object
    def __init__(self, x, y):
        super().__init__(x - BALL_RADIUS, y - BALL_RADIUS, BALL_RADIUS * 2, BALL_RADIUS * 2) # Inherit coords from 'GameObject' class
        self.reset() # Run the reset module (Simplifies the code)


    def reset(self):
        '''
        Resetting the ball, where it resets the ball when a new ball is spawned, or for very beginning, or for new life
        '''
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.speed_x = BALL_SPEED * random.choice([-1, 1])
        self.speed_y = -BALL_SPEED



    def move(self):
        '''
        Moving the ball on the screen, where there is both movement in x and y-directions
        Has position correction, so the ball doesn't get stuck in the walls
        '''
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        # Wall collisions with position correction
        if self.rect.left <= 0:
            self.rect.left = 0
            self.speed_x *= -1

        elif self.rect.right >= SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
            self.speed_x *= -1

        if self.rect.top <= 0:
            self.rect.top = 0
            self.speed_y *= -1
    


    def draw(self):
        '''
        Drawing the ball on the actual screen
        '''

        pygame.draw.circle(screen, RED, self.rect.center, BALL_RADIUS)
