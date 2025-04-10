# models/paddle.py - Paddle Class

import pygame
from constants import * 
from models.game_object import GameObject

class Paddle(GameObject):
    # Initialising Paddle Object
    def __init__(self):
        width, height = PADDLE_WIDTH, PADDLE_HEIGHT
        x = (SCREEN_WIDTH - width) // 2
        y = SCREEN_HEIGHT - height - 30
        super().__init__(x, y, width, height) # Sends coords to 'GameObject' class to make rect
        self.speed = PADDLE_SPEED
        



    def move(self, keys):
        '''
        Moving the paddle on the screen
        Handles player input with left and right arrows pressed by user
        '''

        # If left key pressed, and already not at border of screen
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed # Increase the speed left
        
        # If right key pressed, and already not at border of screen
        if keys[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += self.speed # Increase the speed right


    def draw(self):
        '''
        Drawing the paddle on the screen
        '''

        pygame.draw.rect(screen, WHITE, self.rect)