import pygame
from constants import *

def draw_game_objects(screen, balls, paddle, active_bricks, score):
    screen.fill(BLACK)
    for ball in balls:
        ball.draw(screen)
    paddle.draw(screen)
    for brick in active_bricks:
        brick.draw(screen)
    font = pygame.font.SysFont(None, 36)
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, SCREEN_HEIGHT - 40))

def display_message(screen, message):
    font = pygame.font.SysFont(None, 74)
    text = font.render(message, True, WHITE)
    screen.blit(text, (SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2))
    pygame.display.flip()
    pygame.time.wait(3000)