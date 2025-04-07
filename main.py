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
    def __init__(self, x, y, radius, speed_x, speed_y):
        super().__init__(x - radius, y - radius, radius * 2, radius * 2) # Inherit coords from 'GameObject' class
        self.radius = radius # Ball radius
        self.speed_x = speed_x # Ball speed x-component
        self.speed_y = speed_y # Ball speed y-component

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
        pygame.draw.circle(screen, RED, self.rect.center, self.radius)

    # Resetting the ball
    def reset(self):
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.speed_x = 5 * random.choice([-1, 1])
        self.speed_y = -5




# Paddle Class
class Paddle(GameObject):
    # Initialising Paddle Object
    def __init__(self, x, y, width, height, speed):
        super().__init__(x, y, width, height) # Inherit coords from 'GameObject' class
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
class PowerUp(GameObject):
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
                if brick.brick_type == "normal":
                    active_bricks.remove(brick)
                    score += 10 # Increase score

                    if random.randint(1,8) == 1:
                        powerups.append(PowerUp(brick.rect.centerx, brick.rect.centery))
        
                    ball.speed_y *= -1
                
                # Indestructible blocks, just bounce back
                elif brick.brick_type == "indestructible":
                    ball.speed_y *= -1
            

                # Bomb blocks, need to remove every block around it
                elif brick.brick_type == "bomb":
                    # Remove bomb brick
                    active_bricks.remove(brick)
                    score += 20  # Extra points for bomb bricks
                    ball.speed_y *= -1
                    
                    # Find and remove adjacent bricks
                    bomb_x, bomb_y = brick.rect.x, brick.rect.y
                    directions = [(0, -BRICK_HEIGHT), (0, BRICK_HEIGHT),  # up, down
                                 (-BRICK_WIDTH, 0), (BRICK_WIDTH, 0)]     # left, right
                    
                    for dx, dy in directions:
                        for other_brick in active_bricks[:]:
                            if (other_brick.rect.x == bomb_x + dx and 
                                other_brick.rect.y == bomb_y + dy and
                                other_brick.brick_type != "indestructible"):  # Don't remove indestructible bricks
                                active_bricks.remove(other_brick)
                                score += 5  # Small bonus for adjacent bricks


    # Powerup collision with paddle
    for powerup in powerups[:]:
        if powerup.check_collision(paddle):
            powerups.remove(powerup)
            new_ball = Ball(paddle.rect.centerx, paddle.rect.top - 10, 10, 5 * random.choice([-1, 1]), -5) # Spawn new ball at center of paddle (Using paddle rect)
            balls.append(new_ball)

    return score # Updated score when hit a brick
    



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
def display_message(message):
    font = pygame.font.SysFont(None, 74)
    text = font.render(message, True, WHITE) # Where actual message goes
    screen.blit(text, (SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2))
    pygame.display.flip()
    pygame.time.wait(3000) # 3 second delay to add tension :)




# Main game function
def main():

    # Initialising ball and paddle objects
    ball = Ball(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, 10, 5 * random.choice([-1, 1]), -5)
    paddle = Paddle((SCREEN_WIDTH - 100) // 2, SCREEN_HEIGHT - 30, 100, 20, 8)

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

        for ball in balls[:]:
            print(ball.speed_y)
            ball.move()
            if ball.rect.top >= SCREEN_HEIGHT:
                balls.remove(ball)

        # Check collisions
        score = check_collisions(paddle, balls, active_bricks, powerups, score)

        # Draw game objects
        draw_game_objects(balls, paddle, active_bricks, powerups, score, lives, current_level)


        # Game over condition
        if not balls:
            lives -= 1
            if lives > 0:
                balls = [Ball(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, 10, 5 * random.choice([-1, 1]), -5)]  # Reset balls
            else:
                display_message("GAME OVER")
                running = False


        # Level completed condition
        if not any(brick.brick_type == "normal" for brick in active_bricks):
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


# Running the game
if __name__ == "__main__":
    main()