# models/game_class.py - The game class

import pygame
import random
from constants import *
from models.paddle import Paddle
from models.ball import Ball
from models.brick import Brick
from models.boss_brick import BossBrick
from models.powerup import PowerUp
from utils.get_font import get_font


# THE GAME CLASS
class BrickBlitz:

    # Since no parameters, just call the function which resets the game (Also starts a new game)
    def __init__(self):
        self.reset_game()
    
    def reset_game(self):
        '''
        Function to reset the game, re-initialises all the game properties to start a fresh game
        '''
        self.paddle = Paddle()
        self.balls = [Ball(SCREEN_WIDTH//2, SCREEN_HEIGHT//2)]
        self.powerups = []
        self.current_level = 1
        self.active_bricks = self.generate_bricks(self.current_level)
        self.score = 0
        self.lives = 3

        self.all_game_objects = []
        



    # Generating the bricks for a specific level (Initialising brick objects)
    def generate_bricks(self, level):
        '''
        Generating all the bricks for the levels of the game
        '''

        # Level designs (0 = empty, 1 = normal, 2 = indestructible, 3 = bomb)
        level_designs = {
            1: [
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            ],
            2: [
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [1, 2, 1, 2, 1, 2, 1, 2, 1, 2],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            ],
            3: [
                [2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [1, 3, 1, 3, 1, 3, 1, 3, 1, 3],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            ],
            4: [
                [3, 1, 3, 1, 3, 1, 3, 1, 3, 1],
                [1, 3, 1, 3, 1, 3, 1, 3, 1, 3],
                [3, 2, 3, 2, 3, 2, 3, 2, 3, 2],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [3, 1, 3, 1, 3, 1, 3, 1, 3, 1]
            ]
        }
        
        active_bricks = []
        

        if level == 5:  # Boss level
            return [BossBrick(SCREEN_WIDTH//2 - 100, 50)]
        
        if level not in level_designs:
            return active_bricks
        
        design = level_designs[level]
        
        for row_idx, row in enumerate(design):
            for col_idx, brick_type_code in enumerate(row):
                if brick_type_code == 0:
                    continue
                
                x = col_idx * BRICK_WIDTH
                y = row_idx * BRICK_HEIGHT  # Start from top with no gap
                
                if brick_type_code == 1:
                    brick = Brick(x, y, "normal")
                elif brick_type_code == 2:
                    brick = Brick(x, y, "indestructible")
                elif brick_type_code == 3:
                    brick = Brick(x, y, "bomb")
                
                active_bricks.append(brick)
        
        return active_bricks




    # Function to update game objects
    def update_game_objects(self):
        '''
        Updating all objects in the playing part of the game
        '''
        # Moving all objects
        key_pressed = pygame.key.get_pressed()
        self.paddle.move(key_pressed) # Move paddle


        for ball in self.balls[:]:
            ball.move() # Move all the balls
        
            if ball.rect.top >= SCREEN_HEIGHT: # If ball goes under paddle, remove it
                self.balls.remove(ball)
            

        for powerup in self.powerups[:]:
            powerup.move() # Move all powerups

            if powerup.rect.top >= SCREEN_HEIGHT: # If powerup goes under paddle, remove it
                self.powerups.remove(powerup)



        for ball in self.balls:
            self.handle_paddle_collision(ball)
            self.score += self.handle_brick_collision(ball)
            
        self.handle_powerup_collision()


        # Game over condition with just the boss level
        for brick in [brick for brick in self.active_bricks if isinstance(brick, BossBrick)]: # Loop through every boss brick
            self.lives -= self.handle_boss_behavior(brick) # Operation for finding current lives

            # Game over condition (Explained in other parts of code)
            if self.lives <= 0:
                return STATE_GAMEOVER



        # Game over condition
        if not self.balls:
            self.lives -= 1
            if self.lives > 0:
                self.balls = [Ball(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]  # Reset balls
                            
            else:
                return STATE_GAMEOVER


        # Level completed condition
        if self.check_level_complete():
            # STUD: ACCOUNTING FOR BOSS LEVEL
            if self.current_level < 4:
                self.current_level += 1 # Increase level
                self.active_bricks = self.generate_bricks(self.current_level)  # Generate next level bricks
                self.balls = [Ball(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]  # Reset balls
                self.powerups = []  # Reset power-ups
                return STATE_LEVEL_TRANSITION


            # If level 5, just display a "To be continued..." message, as will most likely be a boss fight
            elif self.current_level == 4:
                self.current_level = 5 # Go to level 5
                self.active_bricks = self.generate_bricks(self.current_level) # Generate the next level bricks
                self.balls = [Ball(SCREEN_WIDTH//2, SCREEN_HEIGHT//2)] # Reset balls
                self.powerups = [] # Reset power-ups
                return STATE_LEVEL_TRANSITION


            # If not in levels 1,2,3,4 (In level 5), and has just finished the level -> Won the game
            else:
                return STATE_WIN

        
        # If not any other state, keep going with game
        return STATE_PLAYING





    # Drawing all game objects
    def draw_game_objects(self):
        '''
        Drawing all the objects in the playing screen of the game
        '''

        # DRAWING THE GRADIENT BACKGROUND
        for y in range(SCREEN_HEIGHT):
            color = (max(0, 10 - y//60), max(0, 20 - y//40), max(30, 50 - y//30))
            pygame.draw.line(screen, color, (0, y), (SCREEN_WIDTH, y))


        self.all_game_objects = []
        self.all_game_objects.extend(self.balls)
        self.all_game_objects.append(self.paddle)
        self.all_game_objects.extend(self.powerups)
        self.all_game_objects.extend(self.active_bricks)
        

        # Polymorphic drawing - Draws all objects
        for obj in self.all_game_objects:
            obj.draw()


        # Draw all active bricks on screen
        for brick in self.active_bricks:
            #brick.draw()

            if isinstance(brick, BossBrick):
                for projectile in brick.projectiles:
                    projectile.draw()





        # Draw all balls on screen
        #for ball in self.balls:
        #    ball.draw()


        # Draw all powerups on screen
        #for powerup in self.powerups:
        #    powerup.draw()


        # Draw paddle on screen
        #self.paddle.draw()


        # Writing all the texts on screen
        font = get_font(24)
        score_text = font.render(f"Score: {self.score}", True, WHITE)
        lives_text = font.render(f"Lives: {self.lives}", True, WHITE)
        level_text = font.render(f"Level: {self.current_level}", True, WHITE)

        screen.blit(score_text, (10, 10))
        screen.blit(lives_text, (10, 50))
        screen.blit(level_text, (SCREEN_WIDTH - 150, 10))





    def handle_paddle_collision(self, ball):
        '''
        Handles collisions between paddle and ball (With the proper direction control)
        All balls are looped through in actual game loop
        WILL REMOVE LATER: Code changed so ball doesn't get stuck in wall or paddle
        '''

        if ball.rect.colliderect(self.paddle.rect): # Check collision (Simplified using CollideableObject class)
            hit_pos = (ball.rect.centerx - self.paddle.rect.centerx) / (self.paddle.rect.width / 2) # Calculate where ball is relative to center using rect
            ball.speed_x = hit_pos * 5 * 1.5 # Ball speed is 5, and with 1.5 multiplier
            ball.speed_y = -abs(ball.speed_y) # Guarantees upward direction)
            ball.rect.bottom = self.paddle.rect.top # Prevent ball getting stuck in paddle 



    def handle_powerup_collision(self):
        '''
        Handles collisions between powerup and paddle
        '''

        for powerup in self.powerups[:]:
            if powerup.rect.colliderect(self.paddle.rect):
                self.powerups.remove(powerup)
                new_ball = Ball(self.paddle.rect.centerx, self.paddle.rect.top - 10) # Spawn new ball at center of paddle (Using paddle rect)
                self.balls.append(new_ball)




    def handle_brick_collision(self, ball):
        '''
        Handles collisions between the bricks and ball
        '''

        score = 0 # Finding the extra score added on

        for brick in self.active_bricks[:]:
            if ball.rect.colliderect(brick.rect):
                # Changing direction of ball, but making sure ball doesn't get bricks on any side / Go through them
                if abs(ball.rect.bottom - brick.rect.top) < 10 and ball.speed_y > 0:
                    ball.speed_y *= -1
                    ball.rect.bottom = brick.rect.top

                elif abs(ball.rect.top - brick.rect.bottom) < 10 and ball.speed_y < 0:
                    ball.speed_y *= -1
                    ball.rect.top = brick.rect.bottom

                elif abs(ball.rect.right - brick.rect.left) < 10 and ball.speed_x > 0:
                    ball.speed_x *= -1
                    ball.rect.right = brick.rect.left

                elif abs(ball.rect.left - brick.rect.right) < 10 and ball.speed_x < 0:
                    ball.speed_x *= -1
                    ball.rect.left = brick.rect.right
                

                if isinstance(brick, BossBrick):
                    brick.take_hit()
                    score += 5 # Hitting boss once = 5 points
                    
                    if brick.health <= 0:
                        self.active_bricks.remove(brick) # If boss dead, remove it


                # Normal blocks have chance of spawning power-up, otherwise increase score ans bounce back normally
                if brick.brick_type == "normal":
                    self.active_bricks.remove(brick) # Remove original brick
                    score += 10 # Increase score

                    if random.randint(1,8) == 1:
                        self.powerups.append(PowerUp(brick.rect.centerx, brick.rect.centery))

                
                # Indestructible blocks only bounce back
                elif brick.brick_type == "indestructible":
                    pass # As ball is bounced back either way above

                
                elif brick.brick_type == "bomb":
                    self.active_bricks.remove(brick) # Remove original brick
                    score += 20 # Increase score (Higher because bomb block)

                    # Find and remove the adjance bricks
                    for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)]: # All positions (Up, down, left, right)
                        for other_brick in self.active_bricks[:]: # Loop through all the bricks to find adjacent bricks
                            if (other_brick.rect.x == brick.rect.x + (dx  *BRICK_WIDTH) and other_brick.rect.y == brick.rect.y + (dy * BRICK_HEIGHT) and other_brick.brick_type != "indestructible"): # If the other brick is one of the adjacent bricks
                                self.active_bricks.remove(other_brick) # Remove the adjance bricks
                                score += 5 # Only 5 points for other bricks
                
                break # Save memory

        return score





    def handle_boss_behavior(self, boss):
        '''
        Handling the behaviour of the boss
        '''

        lives_lost = 0 # Amount of lives the user loses
        
        boss.move() # Move boss

        # If boss is in phase 2 or higher, then start shooting projectile
        if boss.phase >= 2:
            boss.shoot_projectile()
        

        for projectile in boss.projectiles[:]:
            projectile.move() # Move each individual projectile

            # If projectile goes under screen, remove it
            if projectile.rect.top >= SCREEN_HEIGHT:
                boss.projectiles.remove(projectile)

            # If projectile collides with paddle, take off a life
            elif projectile.rect.colliderect(self.paddle.rect):
                boss.projectiles.remove(projectile)
                lives_lost += 1
        
        return lives_lost # Operation with actual live count done in main loop





    def check_level_complete(self):
        '''
        Check if the level is complete
        '''

        # If level is less then 5, check if all bomb and normal blocks have been removed
        if self.current_level < 5:
            return not any(brick.brick_type in ("normal", "bomb") for brick in self.active_bricks)
        

        # If level 5, check if boss block has been killed
        else:
            return not any(isinstance(brick, BossBrick) for brick in self.active_bricks)
