# models/button.py - Button Class

import pygame
from constants import *

class Button:
    def __init__(self, pos, text_input, font, base_colour, hovering_colour):
        self.x_pos, self.y_pos = pos # Button position
        self.font = font
        self.base_colour, self.hovering_colour = base_colour, hovering_colour
        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, self.base_colour)

        self.image = pygame.Surface((300, 80), pygame.SRCALPHA) # Surface for button background
        pygame.draw.rect(self.image, (255, 255, 255, 30), (0, 0, 300, 80), border_radius=15) # Draws semi-transparent white background for button
        pygame.draw.rect(self.image, (255, 255, 255, 100), (0, 0, 300, 80), 2, border_radius=15) # Draws the border of the button

        self.rect = self.image.get_rect(center = (self.x_pos, self.y_pos)) # Rect object for button, also easier to make collisions with mouse
        self.text_rect = self.text.get_rect(center = (self.x_pos, self.y_pos)) # Aligns rendered text so its at same spot at button itself


    def update(self, screen):
        '''
        Drawing the button on the screen
        '''
        screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)



    def changeColour(self, position):
        '''
        Changing the colour of the button based on if the users mouse is hovering over the button
        '''

        if self.checkForInput(position):
            self.text = self.font.render(self.text_input, True, self.hovering_colour)
        else:
            self.text = self.font.render(self.text_input, True, self.base_colour)



    def checkForInput(self, position):
        '''
        Checking if mouse is hovering over the button, to change the colour of the button for the hovering effect
        '''

        return position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom)


