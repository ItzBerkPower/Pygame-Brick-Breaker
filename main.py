import pygame
import random
import sys

pygame.init() # Initialise pygame

# Setting screen
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Breakout Game")


# CONSTANTS
BRICK_WIDTH = SCREEN_WIDTH // 10
BRICK_HEIGHT = 30

PADDLE_WIDTH, PADDLE_HEIGHT = 100, 20
PADDLE_SPEED = 8

POWERUP_SIZE = 20

BALL_RADIUS = 10
BALL_SPEED = 5

# Colours
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
LIGHT_GRAY = (150, 150, 150)
ORANGE = (255, 100, 0)
LIGHT_ORANGE = (250, 50, 0)
YELLOW = (255, 255, 0)
PURPLE = (200, 50, 100)
TEXT_COLOUR = (230, 230, 250)
MENU_TITLE_COLOUR = (182, 143, 64) # Oddly specific, but I wanted an exact colour
LIGHT_BLUE = (173, 216, 230)  # Light blue for button text
HOVER_GRAY = (169, 169, 169)  # Gray for hover text


# Game State Constants
STATE_MENU = 0
STATE_PLAYING = 1
STATE_PAUSED = 2
STATE_GAMEOVER = 3
STATE_WIN = 4
STATE_CONTROLS = 5
STATE_LEVEL_TRANSITION = 6


# Load background image
MENU_BACKGROUND = pygame.image.load("menu_background.png").convert()
MENU_BACKGROUND = pygame.transform.scale(MENU_BACKGROUND, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Initialise clock
clock = pygame.time.Clock()




# Button class
class Button:
    def __init__(self, pos, text_input, font, base_colour, hovering_colour):
        self.x_pos, self.y_pos = pos # Button position
        self.font = font
        self.base_colour, self.hovering_colour = base_colour, hovering_colour
        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, self.base_colour)

        self.image = pygame.Surface((300, 80), pygame.SRCALPHA) # Surface for button background
        pygame.draw.rect(self.image, (255, 255, 255, 30), (0, 0, 300, 80), border_radius=15) # Draws semi-transparent white background for button
        pygame.draw.rect(self.image, (255, 255, 255, 100), (0, 0, 300, 80), 2, border_radius=15) # Draws the border of the button

        self.rect = self.image.get_rect(center = (self.x_pos, self.y_pos)) # Rect object for button, also easier to make collisions with mouse
        self.text_rect = self.text.get_rect(center = (self.x_pos, self.y_pos)) # Aligns rendered text so its at same spot at button itself


    # Updating the button on screen
    def update(self, screen):
        screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)



    # Change the colour of the button when hovered over (For effect)
    def changeColour(self, position):
        if self.checkForInput(position):
            self.text = self.font.render(self.text_input, True, self.hovering_colour)
        else:
            self.text = self.font.render(self.text_input, True, self.base_colour)



    # Check if mouse on top of button
    def checkForInput(self, position):
        return position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom)



# Font helper function
def get_font(size):
    return pygame.font.SysFont("Comic Sans MS", size)



# Base 'GameObject' Class
class GameObject:
    # Initialise Game Object (Currently only coordinates)
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height) # Add rect for collision detection

    def draw(self):
        pass # Will be overridden by child classes

    def move(self):
        pass # Will be overridden by child classes

    def check_collision(self, other_object):
        return self.rect.colliderect(other_object.rect)





# Ball Class
class Ball(GameObject):
    # Initialising Ball object
    def __init__(self, x, y):
        super().__init__(x - BALL_RADIUS, y - BALL_RADIUS, BALL_RADIUS * 2, BALL_RADIUS * 2) # Inherit coords from 'GameObject' class
        self.reset() # Run the reset module (Simplifies the code)


    # Resetting the ball (Also for beginning)
    def reset(self):
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.speed_x = BALL_SPEED * random.choice([-1, 1])
        self.speed_y = -BALL_SPEED


    # Movement of ball
    def move(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        # Wall collisions with position correction
        if self.rect.left <= 0:
            self.rect.left = 0
            self.speed_x *= -1

        elif self.rect.right >= SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
            self.speed_x *= -1

        if self.rect.top <= 0:
            self.rect.top = 0
            self.speed_y *= -1
    

    # Function with drawing ball on actual screen
    def draw(self):
        pygame.draw.circle(screen, RED, self.rect.center, BALL_RADIUS)






# Paddle Class
class Paddle(GameObject):
    # Initialising Paddle Object
    def __init__(self):
        width, height = PADDLE_WIDTH, PADDLE_HEIGHT
        x = (SCREEN_WIDTH - width) // 2
        y = SCREEN_HEIGHT - height - 30
        super().__init__(x, y, width, height) # Sends coords to 'GameObject' class to make rect
        self.speed = PADDLE_SPEED
        


    # Movement of the Paddle
    def move(self, keys):
        # If left key pressed, and already not at border of screen
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed # Increase the speed left
        
        # If right key pressed, and already not at border of screen
        if keys[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += self.speed # Increase the speed right


    # Function for drawing paddle on actual screen
    def draw(self):
        pygame.draw.rect(screen, WHITE, self.rect)




# Power-Up Class
class PowerUp(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y, POWERUP_SIZE, POWERUP_SIZE) # Inherit coords from 'GameObject' class
        self.active = True # Is on the map or not
        self.speed = 2

    def move(self):
        self.rect.y += self.speed  # Move the power-up down the screen (Down the screen is positive TOOK SO LONG TO UNDERSTAND)

    # Draw the power-up on the screen
    def draw(self):
        if self.active:
            pygame.draw.rect(screen, RED, self.rect)





# Brick Class
class Brick(GameObject):
    # Initialising the Brick Object
    def __init__(self, x, y, brick_type = "normal"):
        super().__init__(x, y, BRICK_WIDTH, BRICK_HEIGHT) 
        self.brick_type = brick_type # Type of brick

    # Function for drawing brick on actual screen
    def draw(self):
        if self.brick_type == "normal":
            pygame.draw.rect(screen, GREEN, self.rect) # Rectangle border
            inner_rect = self.rect.inflate(-4, -4)  # Shrink the rectangle to put an actual border
            pygame.draw.rect(screen, BLUE, inner_rect) # Draw the inner rectangle (Just fill with blue)

        elif self.brick_type == "indestructible":
            pygame.draw.rect(screen, GRAY, self.rect)
            inner_rect = self.rect.inflate(-4, -4)
            pygame.draw.rect(screen, LIGHT_GRAY, inner_rect)

        elif self.brick_type == "bomb":
            pygame.draw.rect(screen, ORANGE, self.rect)  # Orange colour
            inner_rect = self.rect.inflate(-4, -4)
            pygame.draw.rect(screen, LIGHT_ORANGE, inner_rect)





# Projectile Class
class Projectile(GameObject):
    def __init__(self, x, y):
        super().__init__(x - 5, y, 10, 10)
        self.speed = 7
    
    def move(self):
        self.rect.y += self.speed
    
    def draw(self):
        pygame.draw.circle(screen, YELLOW, self.rect.center, 5)





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


    # Moves only left and right
    def move(self):
        self.rect.x += self.speed * self.direction
        if self.rect.right >= SCREEN_WIDTH or self.rect.left <= 0:
            self.direction *= -1
    

    # Shoots projectile, though only after stage 2
    def shoot_projectile(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > 2000:  # Shoot every 2 seconds
            self.last_shot = now
            self.projectiles.append(Projectile(self.rect.centerx, self.rect.bottom))
    

    # Hitting the boss with the ball
    def take_hit(self):
        self.health -= 1
        if self.health == 7:
            self.phase = 2
            self.speed = 3
        elif self.health == 3:
            self.phase = 3
            self.speed = 4
    
    
    # Drawing the boss on screen
    def draw(self):
        pygame.draw.rect(screen, self.phase_colours[self.phase], self.rect)
        health_width = (self.width * self.health) // 10
        pygame.draw.rect(screen, (0, 255, 0), (self.rect.x, self.rect.y - 10, health_width, 5))









class GameStateManager:
    def __init__(self):
        self.state = STATE_MENU # Initial state is menu
        self.game = None
        self.level_transition_timer = 0
        self.level_transition_text = ""
        
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
            Button((SCREEN_WIDTH//2, 370), "Main Menu", get_font(20), LIGHT_BLUE, HOVER_GRAY) # Main Menu -> Back to main menu
        ]
        

        # Buttons on the game over screen (When you lose the game)
        self.game_over_buttons = [
            Button((SCREEN_WIDTH//2, 350), "Play Again", get_font(20), LIGHT_BLUE, HOVER_GRAY), # Play Again -> Back to start of game
            Button((SCREEN_WIDTH//2, 450), "Main Menu", get_font(20), LIGHT_BLUE, HOVER_GRAY) # Main Menu -> Back to main menu
        ]
    


    # Changing the state of the game function
    def change_state(self, new_state):
        # If state is quit, then quit the game
        if new_state == "quit":
            pygame.quit()
            sys.exit()
        

        # If state is the playing state, but game hasn't started yet, then create a new game
        if new_state == STATE_PLAYING and not self.game:
            self.game = BreakoutGame()
            self.level_transition_text = f"Level {self.game.current_level}"
            self.level_transition_timer = pygame.time.get_ticks()
            new_state = STATE_LEVEL_TRANSITION
        
        self.state = new_state # Update the state variable
    


    # Handling the events (Eg. Clicking buttons, Hovering Over Buttons, Pausing the Game, etc.)
    def handle_events(self, events):
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
                        # STUD: Whole class is technically a stud, this game state manager requires a game class, so I don't know if I will even use this class or not
                        #self.game = BreakoutGame() # Create a new instance of Game class, hence creating a new game
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
            

            # If no button clicked in 2 seconds, start the game anyway
            if pygame.time.get_ticks() - self.level_transition_timer > 2000:
                self.change_state(STATE_PLAYING)
                return True
        
        return True # End function after just incase
    

    # Update the game
    def update(self):
        if self.state == STATE_PLAYING and self.game:
            result = self.game.update()
            if result:
                self.change_state(result)
    

    # Drawing the screen compared to what screen it is on (Since inconsistent naming I had to do it this way)
    def draw(self):
        screen.fill(BLACK)
        if self.state == STATE_MENU:
            self.draw_menu()

        elif self.state == STATE_CONTROLS:
            self.draw_controls()

        elif self.state == STATE_PLAYING and self.game:
            self.game.draw()

        elif self.state == STATE_PAUSED and self.game:
            self.game.draw()
            self.draw_pause_screen()

        elif self.state == STATE_GAMEOVER and self.game:
            self.game.draw()
            self.draw_gameover_screen()

        elif self.state == STATE_WIN and self.game:
            self.game.draw()
            self.draw_win_screen()

        elif self.state == STATE_LEVEL_TRANSITION and self.game:
            self.game.draw()
            self.draw_level_transition()


        pygame.display.flip() # Update the screen to display the new changes
    


    # Drawing the menu screen
    def draw_menu(self):
        screen.blit(MENU_BACKGROUND, (0, 0)) # Background picture
        
        title_text = get_font(60).render("Brick Blitz", True, MENU_TITLE_COLOUR) # Drawing the title
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH//2, 100)) # Creating rect object for title
        screen.blit(title_text, title_rect) # Printing title to screen
        
        # Updating all the buttons, to check if they clicked or hovered over
        for button in self.menu_buttons:
            button.update(screen)
        

        # Credit: "By Berkay Topal"
        credit_font = get_font(20)
        credit_text = credit_font.render("By Berkay Topal", True, WHITE)
        credit_rect = credit_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT - 30))
        screen.blit(credit_text, credit_rect)
    



    # Drawing the controls screen
    def draw_controls(self):
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
        

        # Update the back button, to check if they clicked or hovered over
        self.back_button.update(screen)
    


    # Drawing the pause screen
    def draw_pause_screen(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA) # Making the screen a bit transparent to make the text more visible IS SO COOL
        overlay.fill((0, 0, 0, 180)) # Actually filling it in with the alpha value of 180, making it semi-transparent   
        screen.blit(overlay, (0, 0)) # Overlay on top of screen, starting from top-left corner
        
        font = get_font(64) # Getting font using helper function

        # Displaying the paused writing
        text = font.render("PAUSED", True, WHITE)
        text_rect = text.get_rect(center=(SCREEN_WIDTH//2, 200))
        screen.blit(text, text_rect)
        

        # Updating all the buttons, to check if they clicked or hovered over
        for button in self.pause_buttons:
            button.update(screen)
    


    # Drawing the game over screen
    def draw_gameover_screen(self):
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
        

        # Updating all the buttons, to check if they clicked or hovered over
        for button in self.game_over_buttons:
            button.update(screen)
    


    # Drawing the win screen
    def draw_win_screen(self):
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
        

        # Updating all the buttons, to check if they clicked or hovered over
        for button in self.game_over_buttons:
            button.update(screen)
    



    # Drawing the level transition screen
    def draw_level_transition(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA) # Making the screen a bit transparent to make the text more visible
        overlay.fill((0, 0, 0, 150)) # Making it semi-transparent
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










# AREA FOR FUNCTIONS FOR GAME

# Generating the bricks for a specific level (Initialising brick objects)
def generate_bricks(level):
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
            [2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
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




# Function to handle quit event
def event_handling():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        
    return True



# Function to update game objects
def update_game_objects(paddle, balls, powerups, keys):
    paddle.move(keys) # Move paddle

    for ball in balls[:]:
        ball.move() # Move all the balls
    
        if ball.rect.top >= SCREEN_HEIGHT: # If ball goes under paddle, remove it
            balls.remove(ball)
        

    for powerup in powerups[:]:
        powerup.move() # Move all powerups

        if powerup.rect.top >= SCREEN_HEIGHT: # If powerup goes under paddle, remove it
            powerups.remove(powerup)


    return powerups







def handle_paddle_collision(ball, paddle):
    '''
    Handles collisions between paddle and ball (With the proper direction control)
    All balls are looped through in actual game loop
    WILL REMOVE LATER: Code changed so ball doesn't get stuck in wall or paddle
    '''

    if ball.rect.colliderect(paddle.rect): # Check collision (Simplified using CollideableObject class)
        hit_pos = (ball.rect.centerx - paddle.rect.centerx) / (paddle.rect.width / 2) # Calculate where ball is relative to center using rect
        ball.speed_x = hit_pos * 5 * 1.5 # Ball speed is 5, and with 1.5 multiplier
        ball.speed_y = -abs(ball.speed_y) # Guarantees upward direction)
        ball.rect.bottom = paddle.rect.top # Prevent ball getting stuck in paddle 




def handle_powerup_collision(powerups, paddle, balls):
    '''
    Handles collisions between powerup and paddle
    '''

    for powerup in powerups[:]:
        if powerup.rect.colliderect(paddle.rect):
            powerups.remove(powerup)
            new_ball = Ball(paddle.rect.centerx, paddle.rect.top - 10) # Spawn new ball at center of paddle (Using paddle rect)
            balls.append(new_ball)


def handle_brick_collision(ball, active_bricks, powerups):
    '''
    Handles collisions between the bricks and ball
    '''

    score = 0 # Finding the extra score added on

    for brick in active_bricks[:]:
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
                    active_bricks.remove(brick) # If boss dead, remove it


            # Normal blocks have chance of spawning power-up, otherwise increase score ans bounce back normally
            if brick.brick_type == "normal":
                active_bricks.remove(brick) # Remove original brick
                score += 10 # Increase score

                if random.randint(1,8) == 1:
                    powerups.append(PowerUp(brick.rect.centerx, brick.rect.centery))

            
            # Indestructible blocks only bounce back
            elif brick.brick_type == "indestructible":
                pass # As ball is bounced back either way above

            
            elif brick.brick_type == "bomb":
                active_bricks.remove(brick) # Remove original brick
                score += 20 # Increase score (Higher because bomb block)

                # Find and remove the adjance bricks
                for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)]: # All positions (Up, down, left, right)
                    for other_brick in active_bricks[:]: # Loop through all the bricks to find adjacent bricks
                        if (other_brick.rect.x == brick.rect.x + (dx  *BRICK_WIDTH) and other_brick.rect.y == brick.rect.y + (dy * BRICK_HEIGHT) and other_brick.brick_type != "indestructible"): # If the other brick is one of the adjacent bricks
                            active_bricks.remove(other_brick) # Remove the adjance bricks
                            score += 5 # Only 5 points for other bricks
            
            break # Save memory

    return score



# Drawing all game objects
def draw_game_objects(balls, paddle, active_bricks, powerups, score, lives, level):
    screen.fill(BLACK) # Fill screen black

    # Draw all balls on screen
    for ball in balls:
        ball.draw()

    # Draw paddle on screen
    paddle.draw()

    # Draw all active bricks on screen
    for brick in active_bricks:
        brick.draw()

        if isinstance(brick, BossBrick):
            for projectile in brick.projectiles:
                projectile.draw()


    # Draw all powerups on screen
    for powerup in powerups:
        powerup.draw()


    font = pygame.font.SysFont(None, 36)
    score_text = font.render(f"Score: {score}", True, WHITE)
    lives_text = font.render(f"Lives: {lives}", True, WHITE)
    level_text = font.render(f"Level: {level}", True, WHITE)

    screen.blit(score_text, (10, 10))
    screen.blit(lives_text, (10, 50))
    screen.blit(level_text, (SCREEN_WIDTH - 150, 10))



# Displaying update messages on screen (At end of level, etc.)
def display_message(message, duration = 3000):
    font = pygame.font.SysFont(None, 74)
    text = font.render(message, True, WHITE) # Where actual message goes
    screen.blit(text, (SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2))
    pygame.display.flip()
    pygame.time.wait(duration) # 3 second delay to add tension :)



def check_level_complete(active_bricks, current_level):
    '''
    Check if the level is complete
    '''

    if current_level < 5:
        return not any(brick.brick_type in ("normal", "bomb") for brick in active_bricks)
    
    # STUD: If I do add a boss level
    #else:
    #    return not any(isinstance(brick, BossBrick) for brick in active_bricks)



def handle_boss_behavior(boss, paddle):
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
        elif projectile.rect.colliderect(paddle.rect):
            boss.projectiles.remove(projectile)
            lives_lost += 1
    
    return lives_lost # Operation with actual live count done in main loop



# Main game function
def main():

    # Initialising ball and paddle objects
    ball = Ball(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    paddle = Paddle()

    # Variables:
    score = 0
    powerups = [] # List of power-ups
    balls = [ball] # List of all balls
    current_level = 5
    active_bricks = generate_bricks(current_level)
    lives = 3


    # Game loop
    running = True

    while running:
        running = event_handling()

        # Moving all objects
        key_pressed = pygame.key.get_pressed()
        powerups = update_game_objects(paddle, balls, powerups, key_pressed)

        
        for ball in balls:
            handle_paddle_collision(ball, paddle)
            score += handle_brick_collision(ball, active_bricks, powerups)
        
        handle_powerup_collision(powerups, paddle, balls)


        # Game over condition with just the boss level
        for brick in [brick for brick in active_bricks if isinstance(brick, BossBrick)]: # Loop through every boss brick
            lives -= handle_boss_behavior(brick, paddle) # Operation for finding current lives

            # Game over condition (Explained in other parts of code)
            if lives <= 0:
                display_message("GAME OVER")
                running = False



        # Game over condition
        if not balls:
            lives -= 1
            if lives > 0:
                balls = [Ball(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]  # Reset balls
                         
            else:
                display_message("GAME OVER")
                running = False


        # Level completed condition
        if check_level_complete(active_bricks, current_level):
            # STUD: ACCOUNTING FOR BOSS LEVEL
            if current_level < 4:
                display_message(f"Level {current_level} Completed")
                
                current_level += 1 # Increase level
                active_bricks = generate_bricks(current_level)  # Generate next level bricks
                balls = [Ball(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]  # Reset balls
                powerups = []  # Reset power-ups


            # If level 5, just display a "To be continued..." message, as will most likely be a boss fight
            elif current_level == 4:
                current_level = 5 # Go to level 5

                display_message("BOSS LEVEL!") # Adding a dramatic effect :)

                active_bricks = generate_bricks(current_level) # Generate the next level bricks
                balls = [Ball(SCREEN_WIDTH//2, SCREEN_HEIGHT//2)] # Reset balls
                powerups = [] # Reset power-ups



            else:
                display_message("YOU WIN!")
                running = False



        # Update display
        screen.fill(BLACK)
        draw_game_objects(balls, paddle, active_bricks, powerups, score, lives, current_level) # Draw all game objects
        pygame.display.flip()
        clock.tick(60)


    # Quit Pygame
    pygame.quit()
    sys.exit()


# Running the game
if __name__ == "__main__":
    main()