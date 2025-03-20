import pygame
from models.game_object import GameObject
from constants import GREEN, BLUE

class Brick(GameObject):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)

    def draw(self, screen):
        pygame.draw.rect(screen, GREEN, self.rect)
        inner_rect = self.rect.inflate(-4, -4)
        pygame.draw.rect(screen, BLUE, inner_rect)