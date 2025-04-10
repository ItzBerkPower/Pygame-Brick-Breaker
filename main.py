# main.py - Main code file

import pygame
import sys

from models.game_state_manager import GameStateManager
from constants import *

pygame.init() # Initialise pygame

# Setting screen
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
pygame.display.set_caption("Breakout Game")




# Initialise clock
clock = pygame.time.Clock()


# Main game function
def main():
    try:
        state_manager = GameStateManager()
        running = True
        

        # Game loop
        running = True

        while running:
            # Catching any errors that run in while loop
            try:
                events = pygame.event.get()
                running = state_manager.handle_events(events)


                state_manager.update()
                state_manager.draw()
                

                clock.tick(60)


            except Exception as e:
                print(f"Error during game loop: {e}")
                state_manager.change_state(STATE_MENU) # Attempt to recover by resetting the game state


    # Catch any potential errors
    except Exception as e:
        print(f"Fatal error: {e}") # Print fatal error to terminal

        # Show error message to user before quitting
        screen.fill(BLACK)
        font = pygame.font.SysFont(None, 36)
        error_text = font.render("A fatal error occurred. The game will now close.", True, RED)
        screen.blit(error_text, (SCREEN_WIDTH//2 - error_text.get_width()//2, SCREEN_HEIGHT//2))

        pygame.display.flip()
        pygame.time.wait(3000)


    # Quit the game
    finally:
        pygame.quit()
        sys.exit()
        


    # Quit Pygame
    pygame.quit()
    sys.exit()



# Running the game
if __name__ == "__main__":
    main()
