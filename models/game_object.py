# models/game_object.py - The GameObject Class

import pygame

class GameObject:
    # Initialise Game Object (Currently only coordinates)
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height) # Add rect for collision detection

    def draw(self):
        raise NotImplementedError("Subclasses must implement draw()")
        # pass

    def move(self):
        # Not this, as the brick doesn't move
        # raise NotImplementedError("Subclasses must implement move()")
        pass

    def check_collision(self, other_object):
        return self.rect.colliderect(other_object.rect)