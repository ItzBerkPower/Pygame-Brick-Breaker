import pygame
import random
from constants import *
from models.paddle import Paddle
from models.ball import Ball
from models.brick import Brick
from utils.game_logic import generate_bricks
from utils.renderer import draw_game_objects, display_message
from utils.collision_handler import check_collisions
from utils.game_logic import update_game_objects, event_handling

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Breakout Game")
    clock = pygame.time.Clock()

    # Initialize game objects
    ball = Ball(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, 10, 5 * random.choice([-1, 1]), -5)
    paddle = Paddle((SCREEN_WIDTH - 100) // 2, SCREEN_HEIGHT - 30, 100, 20, 8)
    balls = [ball]
    score = 0
    current_level = 1
    active_bricks = generate_bricks(current_level)

    # Game loop
    running = True
    while running:
        running = event_handling()
        key_pressed = pygame.key.get_pressed()
        update_game_objects(paddle, balls, key_pressed)
        score = check_collisions(paddle, balls, active_bricks, score)
        draw_game_objects(screen, balls, paddle, active_bricks, score)

        # Game over condition
        if all(ball.rect.bottom >= SCREEN_HEIGHT for ball in balls):
            display_message(screen, "GAME OVER")
            running = False

        # Level completed condition
        if not active_bricks:
            display_message(screen, f"Level {current_level} Completed")
            running = False

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()