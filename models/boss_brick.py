# models/boss_brick.py - BossBrick Class and Projectile Class

import pygame
from constants import *
from models.game_object import GameObject
from models.brick import Brick

class BossBrick(Brick):
    def __init__(self, x, y):
        super().__init__(x, y, "boss") # Brick type = "boss"
        self.width, self.height = 200, 40
        self.rect = pygame.Rect(x, y, self.width, self.height)

        # All properties of the boss
        self.health = 10
        self.phase = 1
        self.speed = 2
        self.direction = 1
        self.projectiles = []
        self.last_shot = 0
        self.phase_colours = {
            1: (200, 50, 50),    # Red
            2: (200, 100, 50),   # Orange
            3: PURPLE            # Purple
        }


    def move(self):
        '''
        Boss moving, where it only moves left and right across the screen, with the y-component staying constant
        '''
        self.rect.x += self.speed * self.direction
        if self.rect.right >= SCREEN_WIDTH or self.rect.left <= 0:
            self.direction *= -1
    


    def shoot_projectile(self):
        '''
        Boss shooting projectiles, only after phase 2 though
        '''
        now = pygame.time.get_ticks()
        if now - self.last_shot > 2000:  # Shoot every 2 seconds
            self.last_shot = now
            self.projectiles.append(Projectile(self.rect.centerx, self.rect.bottom))
    


    def take_hit(self):
        '''
        Doing damage to the boss with the ball
        '''
        self.health -= 1
        if self.health == 7:
            self.phase = 2
            self.speed = 3
        elif self.health == 3:
            self.phase = 3
            self.speed = 4
    
    
    # Drawing the boss on screen
    def draw(self):
        '''DR
        Drawing the boss object on the screen
        '''
        pygame.draw.rect(screen, self.phase_colours[self.phase], self.rect)
        health_width = (self.width * self.health) // 10
        pygame.draw.rect(screen, (0, 255, 0), (self.rect.x, self.rect.y - 10, health_width, 5))





# Projectile Class
class Projectile(GameObject):
    def __init__(self, x, y):
        super().__init__(x - 5, y, 10, 10)
        self.speed = 7
    
    def move(self):
        '''
        Moving the projectile, only in the y-direction, so projectile only moves downwards
        '''

        self.rect.y += self.speed
    

    def draw(self):
        '''
        Drawing the projectile to the screen
        '''

        pygame.draw.circle(screen, YELLOW, self.rect.center, 5)
