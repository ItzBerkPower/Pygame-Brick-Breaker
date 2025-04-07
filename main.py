import pygame
import random

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

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
LIGHT_GRAY = (150,150,150)
ORANGE = (255, 100, 0)
LIGHT_ORANGE = (250,50,0)

# Initialise clock
clock = pygame.time.Clock()


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
            pygame.draw.rect(screen, ORANGE, self.rect)  # Orange color
            inner_rect = self.rect.inflate(-4, -4)
            pygame.draw.rect(screen, LIGHT_ORANGE, inner_rect)





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
    
    bricks = []
    
    # STUD: What the boss brick would look like
    #if level == 5:  # Boss level
    #    return [BossBrick(SCREEN_WIDTH//2 - 100, 50)]
    
    if level not in level_designs:
        return bricks
    
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
            
            bricks.append(brick)
    
    return bricks




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



# Main game function
def main():

    # Initialising ball and paddle objects
    ball = Ball(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    paddle = Paddle()

    # Variables:
    score = 0
    powerups = [] # List of power-ups
    balls = [ball] # List of all balls
    current_level = 3
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
                display_message("To be continued...")
                running = False

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


# Running the game
if __name__ == "__main__":
    main()