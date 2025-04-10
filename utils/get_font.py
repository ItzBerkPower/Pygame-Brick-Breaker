# utils/get_font.py - Font for the text in the game

import pygame

def get_font(size):
    '''
    Font used for all text in game, defined here
    '''

    # Using try-except block in case the font cannot be found
    try:
        return pygame.font.SysFont("Comic Sans MS", size)
    
    except:
        print("Warning: Comic Sans MS font not found, using default font")
        return pygame.font.SysFont(None, size)
