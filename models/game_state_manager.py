# models/game_state_manager.py - Game State Manager class

from constants import *
from models.button import Button
from utils.get_font import get_font
from models.game_class import BrickBlitz
import sys


# Load background image
MENU_BACKGROUND = pygame.image.load("menu_background.png").convert()
MENU_BACKGROUND = pygame.transform.scale(MENU_BACKGROUND, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Game State Manager Class
class GameStateManager:
    def __init__(self):
        self.state = STATE_MENU # Initial state is menu
        self.game = None
        self.level_transition_timer = 0
        self.level_transition_text = ""

        self.transition_alpha = 0
        self.fade_speed = 255 / 30  # Fade over ~0.5s at 60 FPS

        
        # All buttons on the menu
        self.menu_buttons = [
            Button((SCREEN_WIDTH//2, 250), "PLAY", get_font(40), LIGHT_BLUE, HOVER_GRAY), # Play button -> Game
            Button((SCREEN_WIDTH//2, 350), "CONTROLS", get_font(40), LIGHT_BLUE, HOVER_GRAY), # Controls button -> Controls screen
            Button((SCREEN_WIDTH//2, 450), "QUIT", get_font(40), LIGHT_BLUE, HOVER_GRAY) # Quit button -> Quit screen
        ]
        
        self.back_button = Button((SCREEN_WIDTH//2, 550), "BACK", get_font(20), LIGHT_BLUE, HOVER_GRAY) # Back button
        
        # Buttons on the pause screen (When you press ESC)
        self.pause_buttons = [
            Button((SCREEN_WIDTH//2, 300), "Resume", get_font(20), LIGHT_BLUE, HOVER_GRAY), # Resume -> Back to game
            Button((SCREEN_WIDTH//2, 400), "Main Menu", get_font(20), LIGHT_BLUE, HOVER_GRAY) # Main Menu -> Back to main menu
        ]
        

        # Buttons on the game over screen (When you lose the game)
        self.game_over_buttons = [
            Button((SCREEN_WIDTH//2, 350), "Play Again", get_font(20), LIGHT_BLUE, HOVER_GRAY), # Play Again -> Back to start of game
            Button((SCREEN_WIDTH//2, 450), "Main Menu", get_font(20), LIGHT_BLUE, HOVER_GRAY) # Main Menu -> Back to main menu
        ]
    



    def change_state(self, new_state):
        '''
        Changing the game state
        '''
        
        # Handle errors gracefully
        try:
            # If state is quit, then quit the game
            if new_state == "quit":
                pygame.quit()
                sys.exit()
            

            # If state is the playing state, but game hasn't started yet, then create a new game
            if new_state == STATE_PLAYING and not self.game:
                self.game = BrickBlitz()
                self.level_transition_text = f"Level {self.game.current_level}"
                self.level_transition_timer = pygame.time.get_ticks()
                self.transition_alpha = 0
                new_state = STATE_LEVEL_TRANSITION


            # If in the state level transition, but with a game, then change the new text, as a new level has been reached
            elif new_state == STATE_LEVEL_TRANSITION:
                self.level_transition_text = f"Level {self.game.current_level}"
                self.level_transition_timer = pygame.time.get_ticks()
                self.transition_alpha = 0
            
            self.state = new_state # Update the state variable


        except Exception as e:
            print(f"Error changing state: {e}")
            self.state = STATE_MENU # Go back to menu state
            self.game = None # Delete the current game
            
    


    def handle_events(self, events):
        '''
        Handling all of the events in the game (Eg. Clicking Buttons, Hovering Over Buttons, Pausing the Game, etc.)
        '''
        mouse_pos = pygame.mouse.get_pos() # Get position of mouse
        
        # If on main menu screen
        if self.state == STATE_MENU:
            # Check if mouse is on any of buttons, and create hovering effect if so
            for button in self.menu_buttons:
                button.changeColour(mouse_pos)
            

            for event in events:
                # If closing game, no change in state, etc.
                if event.type == pygame.QUIT:
                    return False
                


                if event.type == pygame.MOUSEBUTTONDOWN:

                    # If mouse button on "Play" button, change state to actual game
                    if self.menu_buttons[0].checkForInput(mouse_pos):
                        self.change_state(STATE_PLAYING)
                        return True
                    
                    # If mouse button on "Controls" button, change state to controls menu
                    if self.menu_buttons[1].checkForInput(mouse_pos):
                        self.change_state(STATE_CONTROLS)
                        return True
                    

                    # If mouse button on "Quit" button, quit the game
                    if self.menu_buttons[2].checkForInput(mouse_pos):
                        self.change_state("quit")
                        return True
        


        # If on controls screen
        elif self.state == STATE_CONTROLS:
            self.back_button.changeColour(mouse_pos)
            
            for event in events:
                # If closing game, no change in state
                if event.type == pygame.QUIT:
                    return False
                

                # If clicked on "Back" button, go back to main menu
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.back_button.checkForInput(mouse_pos):
                        self.change_state(STATE_MENU)
                        return True
        



        # If actually playing the game
        elif self.state == STATE_PLAYING:
            for event in events:
                # If closing game, no change in state
                if event.type == pygame.QUIT:
                    return False
                

                # If clicked escape key, go to paused screen
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.change_state(STATE_PAUSED)
                        return True
        



        # If on paused screen
        elif self.state == STATE_PAUSED:
            # Check if hovering over one of the buttons ("Resume" or "Main Menu")
            for button in self.pause_buttons:
                button.changeColour(mouse_pos)
            

            for event in events:
                # If closing game, no change in state
                if event.type == pygame.QUIT:
                    return False
                

                # If clicked on the mouse,
                if event.type == pygame.MOUSEBUTTONDOWN:

                    # If on the "Resume" button, go back to game screen
                    if self.pause_buttons[0].checkForInput(mouse_pos):
                        self.change_state(STATE_PLAYING)
                        return True
                    

                    # If on "Main Menu" button, go back to main menu
                    if self.pause_buttons[1].checkForInput(mouse_pos):
                        self.game = None
                        self.change_state(STATE_MENU)
                        return True
                    

            
        # If either game over, or on the win menu (So either game over screen)
        elif self.state == STATE_GAMEOVER or self.state == STATE_WIN:

            # Check if hovering over any of buttons for hovering effect
            for button in self.game_over_buttons:
                button.changeColour(mouse_pos)
            

            for event in events:
                # If closing game, no change in state
                if event.type == pygame.QUIT:
                    return False
                

                # If button on mouse clicked,
                if event.type == pygame.MOUSEBUTTONDOWN:

                    # If on the "Play Again" button, restart the game
                    if self.game_over_buttons[0].checkForInput(mouse_pos):
                        self.game = BrickBlitz() # Create a new instance of Game class, hence creating a new game
                        self.change_state(STATE_PLAYING)
                        return True
                    

                    # If on the "Main Menu" button, go back to main menu
                    if self.game_over_buttons[1].checkForInput(mouse_pos):
                        self.game = None # End game completely, deleting it
                        self.change_state(STATE_MENU)
                        return True
        


        # If on the initial screen
        elif self.state == STATE_LEVEL_TRANSITION:
            for event in events:
                # If closing game, no change in state
                if event.type == pygame.QUIT:
                    return False
                
                # If clicked the enter key, start the game
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    self.change_state(STATE_PLAYING)
                    return True
            
            # FADING EFFECT
            elapsed_time = pygame.time.get_ticks() - self.level_transition_timer # Time since transition started

            # While below 500, update transition value to get more dark (Less transparency)
            if elapsed_time < 500:
                self.transition_alpha = min(150, self.transition_alpha + self.fade_speed)

            # After 2.5 seconds, start getting less dark (More transparency)
            elif elapsed_time > 2500:
                self.transition_alpha = max(0, self.transition_alpha - self.fade_speed)

            # After 3 seconds, start round
            if elapsed_time > 3000:
                self.change_state(STATE_PLAYING)
                return True

            # PREV VERSION
            # If no button clicked in 2 seconds, start the game anyway
            #if pygame.time.get_ticks() - self.level_transition_timer > 2000:
            #    self.change_state(STATE_PLAYING)
            #    return True
        
        return True # End function after just incase
    

    # Update the game
    def update(self):
        '''
        Updating the game
        '''

        # If currently playing game and there is a game, update all the game objects
        if self.state == STATE_PLAYING and self.game:
            result = self.game.update_game_objects()
            if result != STATE_PLAYING: # If there is a change of state, then change it
                self.change_state(result)
    


    def draw(self):
        '''
        Actually drawing the screens to the screen based on what screen it is currently on

        I had inconsistent naming, so had to do it the long way
        '''
        screen.fill(BLACK) # Resetting the screen

        # Drawing the menu if on menu screen
        if self.state == STATE_MENU:
            self.draw_menu()

        # Drawing the controls if on controls screen
        elif self.state == STATE_CONTROLS:
            self.draw_controls()

        # Drawing the game if on game screen
        elif self.state == STATE_PLAYING and self.game:
            self.game.draw_game_objects()

        # Deawing the paused screen if game is paused
        elif self.state == STATE_PAUSED and self.game:
            self.game.draw_game_objects()
            self.draw_pause_screen()

        # Drawing the game over screen if game is over (Lost)
        elif self.state == STATE_GAMEOVER and self.game:
            self.game.draw_game_objects()
            self.draw_gameover_screen()


        # Drawing the game over screen if game is over (Won)
        elif self.state == STATE_WIN and self.game:
            self.game.draw_game_objects()
            self.draw_win_screen()


        # Drawing the level transition screen
        elif self.state == STATE_LEVEL_TRANSITION and self.game:
            self.game.draw_game_objects()
            self.draw_level_transition()

        pygame.display.flip() # Update the screen to display the new changes
    



    def draw_menu(self):
        '''
        Drawing the main menu screen (Background, buttons, credit)
        '''
        screen.blit(MENU_BACKGROUND, (0, 0)) # Background picture
        
        title_text = get_font(60).render("Brick Blitz", True, MENU_TITLE_COLOUR) # Drawing the title
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH//2, 100)) # Creating rect object for title
        screen.blit(title_text, title_rect) # Printing title to screen
        
        # Drawing all the menu buttons to the screen
        for button in self.menu_buttons:
            button.update(screen)
        

        # Credit: "By Berkay Topal"
        credit_font = get_font(20)
        credit_text = credit_font.render("By Berkay Topal", True, WHITE)
        credit_rect = credit_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT - 30))
        screen.blit(credit_text, credit_rect)
    




    def draw_controls(self):
        '''
        Drawing the controls screen with all the text
        '''
        screen.fill(BLACK) # Background is black
        
        title_text = get_font(40).render("Controls", True, MENU_TITLE_COLOUR) # Drawing the controls title
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH//2, 80))
        screen.blit(title_text, title_rect)
        

        font = get_font(20) # Font through the helper function

        # Writing for control screen, each element in list is a different line on screen
        controls = [
            "Left/Right Arrow Keys - Move Paddle",
            "ESC - Pause Game",
            "Break bricks to score points",
            "Bomb bricks destroy adjacent bricks",
            "Indestructible bricks can't be broken",
            "Collect power-ups for extra balls",
            "Defeat the boss to win!"
        ]

        # Loop through all lines, printing them on a different line on screen
        for i, line in enumerate(controls):
            text = font.render(line, True, WHITE)
            screen.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, 150 + i * 40))  # Moved up to y=150
        

        # Drawing the back button to the screen
        self.back_button.update(screen)
    


    def draw_pause_screen(self):
        '''
        Drawing the screen for when player pauses the screen (By pressing escape key)
        '''
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA) # Making the screen a bit transparent to make the text more visible IS SO COOL
        overlay.fill((0, 0, 0, 180)) # Actually filling it in with the alpha value of 180, making it semi-transparent   
        screen.blit(overlay, (0, 0)) # Overlay on top of screen, starting from top-left corner
        
        font = get_font(64) # Getting font using helper function

        # Displaying the paused writing
        text = font.render("PAUSED", True, WHITE)
        text_rect = text.get_rect(center=(SCREEN_WIDTH//2, 200))
        screen.blit(text, text_rect)
        

        # Drawing the two buttons on the pause menu to the screen
        for button in self.pause_buttons:
            button.update(screen)
    



    def draw_gameover_screen(self):
        '''
        Drawing the screen for "Game Over" when player runs out of lives -> Loses the game
        '''
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA) # Making the screen a bit transparent to make the text more visible
        overlay.fill((0, 0, 0, 180)) # Making it semi-transparent
        screen.blit(overlay, (0, 0)) # Overlay on top of screen, starting from top-left corner
        
        font = get_font(64) # Getting font using helper function

        # Displaying the game over writing
        text = font.render("GAME OVER", True, RED) # Red text for dramatic effect :)
        text_rect = text.get_rect(center=(SCREEN_WIDTH//2, 200))
        screen.blit(text, text_rect)
        
        # Displaying the score on the screen
        score_font = get_font(36) 
        score_text = score_font.render(f"Final Score: {self.game.score}", True, WHITE)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH//2, 280))
        screen.blit(score_text, score_rect)
        

        # Drawing the buttons on the game over screen to the screen (Lost)
        for button in self.game_over_buttons:
            button.update(screen)
    


    def draw_win_screen(self):
        '''
        Drawing the winning screen for the game
        '''
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA) # Making the screen a bit transparent to make the text more visible
        overlay.fill((0, 0, 0, 180)) # Making it semi-transparent
        screen.blit(overlay, (0, 0)) # Overlap on top of screen, starting from top-left corner
        
        font = get_font(64) # Getting font using helper function

        # Displaying the win writing
        text = font.render("YOU WIN!", True, GREEN)
        text_rect = text.get_rect(center=(SCREEN_WIDTH//2, 200))
        screen.blit(text, text_rect)
        

        # Displaying the score on the screen
        score_font = get_font(36)
        score_text = score_font.render(f"Final Score: {self.game.score}", True, WHITE)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH//2, 280))
        screen.blit(score_text, score_rect)
        

        # Drawing the buttons on the game over screen to the screen (Won)
        for button in self.game_over_buttons:
            button.update(screen)
    



    def draw_level_transition(self):
        '''
        Drawing the screen for transitioning between levels
        '''
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA) # Making the screen a bit transparent to make the text more visible
        overlay.fill((0, 0, 0, int(self.transition_alpha))) # Making it semi-transparent with the fading effect
        screen.blit(overlay, (0, 0)) # Overlap on top of screen, starting from top-left corner
        
        font = get_font(64) # Getting font using helper function

        # Displaying the level transition writing
        text = font.render(self.level_transition_text, True, WHITE)
        text_rect = text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
        screen.blit(text, text_rect)
        

        # Displaying the instruction writing (How to start the game)
        instruction_font = get_font(24)
        instruction_text = instruction_font.render("Press ENTER to continue", True, WHITE)
        instruction_rect = instruction_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 80))
        screen.blit(instruction_text, instruction_rect)

