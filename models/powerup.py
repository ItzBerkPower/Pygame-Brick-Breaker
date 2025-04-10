# models/powerup.py - PowerUp class

import pygame
from constants import *
from models.game_object import GameObject


class PowerUp(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y, POWERUP_SIZE, POWERUP_SIZE) # Inherit coords from 'GameObject' class
        self.active = True # Is on the map or not
        self.speed = 2


    def move(self):
        '''
        Moving the powerup, where it only moves in the y-direction, so it moves downwards constantly
        '''

        self.rect.y += self.speed  # Move the power-up down the screen (Down the screen is positive TOOK SO LONG TO UNDERSTAND)


    def draw(self):
        '''
        Drawing the power-ups to the screen
        '''

        if self.active:
            pygame.draw.rect(screen, RED, self.rect)