import pygame
import random

pygame.init() # Initialise pygame

# Setting screen
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Breakout Game")


# CONSTANTS
brick_width = SCREEN_WIDTH // 10
brick_height = 30

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

# Initialise clock
clock = pygame.time.Clock()


# Base 'GameObject' Class
class GameObject:
    # Initialise Game Object (Currently only coordinates)
    def __init__(self, x, y):
        self.x = x # Object x-coord
        self.y = y # Object y-coord


    def draw(self):
        pass # Will be overridden by child classes

    def move(self):
        pass # Will be overridden by child classes



# CollidableObject Class (Inherits From GameObject)
class CollidableObject(GameObject):
    def __init__(self, x, y, width, height):
        super().__init__(x, y)
        self.rect = pygame.Rect(x, y, width, height)  # Add a rect for collision detection

    def check_collision(self, other_object):
        return self.rect.colliderect(other_object.rect)





# Ball Class
class Ball(CollidableObject):
    # Initialising Ball object
    def __init__(self, x, y, radius, speed_x, speed_y):
        super().__init__(x - radius, y - radius, radius * 2, radius * 2) # Inherit coords from 'GameObject' class
        self.radius = radius # Ball radius
        self.speed_x = speed_x # Ball speed x-component
        self.speed_y = speed_y # Ball speed y-component

    # Movement of ball
    def move(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        # Collision with walls => Collide with walls, then go opposite direction
        if self.rect.left <= 0 or self.rect.right >= SCREEN_WIDTH:
            self.speed_x *= -1

        if self.rect.top <= 0:
            self.speed_y *= -1
    

    # Function with drawing ball on actual screen
    def draw(self):
        pygame.draw.circle(screen, RED, self.rect.center, self.radius)

    # Resetting the ball
    def reset(self):
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.speed_x = 5 * random.choice([-1, 1])
        self.speed_y = -5




# Paddle Class
class Paddle(CollidableObject):
    # Initialising Paddle Object
    def __init__(self, x, y, width, height, speed):
        super().__init__(x, y, width, height) # Inherit coords from 'GameObject' class
        self.width = width # Paddle width
        self.height = height # Paddle height
        self.speed = speed # Paddle speed


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
class PowerUp(CollidableObject):
    def __init__(self, x, y):
        super().__init__(x, y, 20, 20) # Inherit coords from 'GameObject' class
        self.active = True # Is on the map or not

    def move(self):
        self.rect.y += 2  # Move the power-up down the screen (Down the screen is positive TOOK SO LONG TO UNDERSTAND)

    # Draw the power-up on the screen
    def draw(self):
        if self.active:
            pygame.draw.rect(screen, RED, self.rect)

    # Check the collision of the power-up with the paddle
    def check_collision(self, paddle):
        if self.active and super().check_collision(paddle): # If collides with paddle
            self.active = False # Delete the powerup
            return True # (So new ball can be spawned)
        return False



# Brick Class
class Brick(CollidableObject):
    # Initialising the Brick Object
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height) 

    # Function for drawing brick on actual screen
    def draw(self):
        pygame.draw.rect(screen, GREEN, self.rect) # Rectangle border
        inner_rect = self.rect.inflate(-4, -4)  # Shrink the rectangle to put an actual border
        pygame.draw.rect(screen, BLUE, inner_rect) # Draw the inner rectangle (Just fill with blue)






# AREA FOR FUNCTIONS FOR GAME

# Generating the bricks for a specific level (Initialising brick objects)
def generate_bricks(level):
    bricks = []

    # Increase the number of rows based on the level
    rows = 4 + level  # Level 1: 5 rows, Level 2: 6 rows, etc.
    for row in range(rows):
        for col in range(SCREEN_WIDTH // brick_width):
            brick = Brick(col * brick_width, row * brick_height, brick_width, brick_height)
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

    for ball in balls:
        ball.move() # Move all the balls

    for powerup in powerups:
        powerup.move() # Move all powerups

    # Remove power-ups that go off-screen
    powerups = [powerup for powerup in powerups if powerup.rect.y < SCREEN_HEIGHT]

    return powerups



# Function to check collisions between objects
def check_collisions(paddle, balls, active_bricks, powerups, score):
    
    # Ball collision with paddle (With proper directional control)
    for ball in balls:
        if ball.check_collision(paddle): # Check collision (Simplified using CollideableObject class)
            hit_position = (ball.rect.centerx - paddle.rect.centerx) / (paddle.rect.width / 2) # Calculate where ball is relative to center using rect
            ball.speed_x = hit_position * 10 # Adjust horizontal speed (Scale by 10)
            ball.speed_y *= -1 # Ball goes back up when hits paddle

        
    # Ball collision with bricks
    for ball in balls:
        for brick in active_bricks[:]:
            if ball.check_collision(brick): # Check collision (Simplified using CollideableObject class)
                active_bricks.remove(brick)
                ball.speed_y *= -1
                score += 10 # Increase score

                if random.randint(1,8) == 1:
                    powerups.append(PowerUp(brick.rect.centerx, brick.rect.centery))
                

    for powerup in powerups[:]:
        if powerup.check_collision(paddle):
            powerups.remove(powerup)
            new_ball = Ball(paddle.rect.centerx, paddle.rect.top - 10, 10, 5 * random.choice([-1, 1]), -5) # Spawn new ball at center of paddle (Using paddle rect)
            balls.append(new_ball)

    return score # Updated score when hit a brick
    

# Drawing all game objects
def draw_game_objects(balls, paddle, active_bricks, powerups, score):
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


    # Display score
    font = pygame.font.SysFont(None, 36)
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, SCREEN_HEIGHT - 40))




# Displaying update messages on screen (At end of level, etc.)
def display_message(message):
    font = pygame.font.SysFont(None, 74)
    text = font.render(message, True, WHITE) # Where actual message goes
    screen.blit(text, (SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2))
    pygame.display.flip()
    pygame.time.wait(3000) # 3 second delay to add tension :)





# Initialising ball and paddle objects
ball = Ball(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, 10, 5 * random.choice([-1, 1]), -5)
paddle = Paddle((SCREEN_WIDTH - 100) // 2, SCREEN_HEIGHT - 30, 100, 20, 8)

# Variables:
score = 0
powerups = [] # List of power-ups
balls = [ball] # List of all balls
current_level = 1
active_bricks = generate_bricks(current_level)


# Game loop
running = True

while running:
    running = event_handling()


    # Moving all objects
    key_pressed = pygame.key.get_pressed()
    powerups = update_game_objects(paddle, balls, powerups, key_pressed)


    # Check collisions
    score = check_collisions(paddle, balls, active_bricks, powerups, score)

    # Draw game objects
    draw_game_objects(balls, paddle, active_bricks, powerups, score)


    # Game over condition
    if all(ball.rect.bottom >= SCREEN_HEIGHT for ball in balls):
        display_message("GAME OVER")
        running = False


    # Level completed condition
    if not active_bricks:
        if current_level < 5:
            display_message(f"Level {current_level} Completed")

            # Moving to next level
            current_level += 1
            active_bricks = generate_bricks(current_level)  # Generate next level bricks
            balls = [Ball(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, 10, 5 * random.choice([-1, 1]), -5)]  # Reset balls
            powerups = []  # Reset power-ups


        # If level 5, just display a "To be continued..." message, as will most likely be a boss fight
        else:
            display_message("To be continued...")
            running = False


    # Update display
    pygame.display.flip()
    clock.tick(60)


# Quit Pygame
pygame.quit()