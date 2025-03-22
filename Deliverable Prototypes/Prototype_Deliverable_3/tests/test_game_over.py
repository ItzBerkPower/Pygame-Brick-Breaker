import unittest

# Accessing a file in a sibling directory
import os, sys
sys.path.insert(1, "/".join(os.path.realpath(__file__).split("/")[0:-2]))

from models.ball import Ball
from models.paddle import Paddle
from models.brick import Brick
from utils.collision_handler import check_collisions
from constants import SCREEN_WIDTH, SCREEN_HEIGHT



class TestGameOver(unittest.TestCase):
    def test_game_over_condition(self):
        '''Testing the game over condition, by simulating all the balls being below the screen'''

        ball = Ball(100, SCREEN_HEIGHT + 10, 10, 5, 5)  # Ball is below the screen
        balls = [ball]

        # Check if all balls are below the screen
        game_over = all(ball.rect.bottom >= SCREEN_HEIGHT for ball in balls)
        self.assertTrue(game_over, "Game over condition should be triggered when all balls are below the screen")
    

    def test_ball_paddle_collision(self):
        '''Testing if the ball speed is reversed when colliding with paddle'''

        paddle = Paddle((SCREEN_WIDTH - 100) // 2, SCREEN_HEIGHT - 30, 100, 20, 8)
        ball = Ball(paddle.rect.centerx, paddle.rect.top - 9, 10, 5, 5)  # Ball just inside paddle (From the top)

        # Initial ball direction
        initial_speed_y = ball.speed_y

        # Simulate the collision in a game scenario
        active_bricks = []  # No bricks for this test
        score = 0
        score = check_collisions(paddle, [ball], active_bricks, score)

        # Check if the ball's direction is reversed
        self.assertNotEqual(ball.speed_y, initial_speed_y, "Ball direction should be reversed after colliding with the paddle")

if __name__ == "__main__":
    unittest.main()