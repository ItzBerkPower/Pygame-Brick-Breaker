# tests/test_paddle.py - TestPaddle Class

import unittest
import pygame
import os
import sys
from pygame.locals import K_LEFT, K_RIGHT

sys.path.insert(1, "/".join(os.path.realpath(__file__).split("/")[0:-2]))

from models.paddle import Paddle
from constants import *



class TestPaddle(unittest.TestCase):
    # Initialise class
    def setUp(self):
        pygame.init() # Initialize pygame (required for testing)
        self.paddle = Paddle() # Same initialisation as actual game

    # Testing for paddle moving left, which is done by pressing left arrow key
    def test_move_left(self):
        keys = {K_LEFT: True, K_RIGHT: False} # Simulate pressing left arrow key
        initial_x = self.paddle.rect.x # Save initial x-coordinate of paddle to compare with final x-coordinate
        self.paddle.move(keys) # Simulate moving the paddle
        self.assertEqual(self.paddle.rect.x, initial_x - self.paddle.speed, "Paddle should move left") # Check if moved

    # Testing for paddle moving right, which is done by pressing right arrow key
    def test_move_right(self):
        keys = {K_LEFT: False, K_RIGHT: True} # Simulate pressing right arrow key
        initial_x = self.paddle.rect.x # Save initial x-coordinate of paddle to compare with final x-coordinate
        self.paddle.move(keys) # Simulate moving the paddle
        self.assertEqual(self.paddle.rect.x, initial_x + self.paddle.speed, "Paddle should move right") # Check if moved

    # Testing for paddle staying within the left wall, which is done by paddle moving left when already at x-coord 0, and seeing if it can keep going
    def test_stay_within_bounds_left(self):
        self.paddle.rect.x = 0 # Start paddle at left edge
        keys = {K_LEFT: True, K_RIGHT: False} # Simulate pressing left arrow key (Moving left)
        self.paddle.move(keys) # Simulate moving the paddle
        self.assertEqual(self.paddle.rect.x, 0, "Paddle shouldn't move beyond the left edge") # Check if paddle has crossed x-coord 0, or is still equal to 0

    # Testing for paddle staying within the right wall, which is done by paddle moving right when already at x-coord of the screen width, and seeing if it can keep going
    def test_stay_within_bounds_right(self):
        self.paddle.rect.x = SCREEN_WIDTH - self.paddle.rect.width # Start paddle at right edge
        keys = {K_LEFT: False, K_RIGHT: True} # Simulate pressing right arrow key (Moving right)
        self.paddle.move(keys) # Simulate moving the paddle
        self.assertEqual(self.paddle.rect.x, SCREEN_WIDTH - self.paddle.rect.width, "Paddle shouldn't move beyond the right edge") # Check if paddle has crossed x-coord of screen width, or is still equal

    # Clean up pygame
    def tearDown(self):
        pygame.quit()

if __name__ == "__main__":
    unittest.main()