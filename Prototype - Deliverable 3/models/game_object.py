import pygame

class GameObject:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)

    def draw(self):
        pass

    def move(self):
        pass

    def check_collision(self, other_object):
        return self.rect.colliderect(other_object.rect)