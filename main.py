import pygame
import random

pygame.init() # Initialise pygame

# Setting screen
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Breakout Game")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

# Initialise clock
clock = pygame.time.Clock()

# Ball Class
class Ball:
    # Initialising Ball object
    def __init__(self, x, y, radius, speed_x, speed_y):
        self.x = x # Ball x-coord
        self.y = y # Ball y-coord
        self.radius = radius # Ball radius
        self.speed_x = speed_x # Ball speed x-component
        self.speed_y = speed_y # Ball speed y-component

    # Movement of ball
    def move(self):
        self.x += self.speed_x
        self.y += self.speed_y

        # Collision with walls => Collide with walls, then go opposite direction
        if self.x <= self.radius or self.x >= SCREEN_WIDTH - self.radius:
            self.speed_x *= -1
        if self.y <= self.radius:
            self.speed_y *= -1
    

    # Function with drawing ball on actual screen
    def draw(self):
        pygame.draw.circle(screen, RED, (int(self.x), int(self.y)), self.radius)

    # Resetting the ball
    def reset(self):
        self.x = SCREEN_WIDTH // 2
        self.y = SCREEN_HEIGHT // 2
        self.speed_x = 5 * random.choice([-1, 1])
        self.speed_y = -5



# Paddle Class
class Paddle:
    # Initialising Paddle Object
    def __init__(self, x, y, width, height, speed):
        self.x = x # Paddle x-coord
        self.y = y # Paddle y-coord
        self.width = width # Paddle width
        self.height = height # Paddle height
        self.speed = speed # Paddle speed


    # Movement of the Paddle
    def move(self, keys):
        # If left key pressed, and already not at border of screen
        if keys[pygame.K_LEFT] and self.x > 0:
            self.x -= self.speed # Increase the speed left
        
        # If right key pressed, and already not at border of screen
        if keys[pygame.K_RIGHT] and self.x < SCREEN_WIDTH - self.width:
            self.x += self.speed # Increase the speed right

    # Function for drawing paddle on actual screen
    def draw(self):
        pygame.draw.rect(screen, WHITE, (self.x, self.y, self.width, self.height))




# Brick Class
class Brick:
    # Initialising the Brick Object
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)

    # Function for drawing brick on actual screen
    def draw(self):
        pygame.draw.rect(screen, GREEN, self.rect) # Rectangle border
        inner_rect = self.rect.inflate(-4, -4)  # Shrink the rectangle to put an actual border
        pygame.draw.rect(screen, BLUE, inner_rect) # Draw the inner rectangle (Just fill with blue)



# Variables:
score = 0

# Initialising ball and paddle objects
ball = Ball(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, 10, 5 * random.choice([-1, 1]), -5)
paddle = Paddle((SCREEN_WIDTH - 100) // 2, SCREEN_HEIGHT - 30, 100, 20, 8)

# Initialising brick objects
brick_width = SCREEN_WIDTH // 10
brick_height = 30
brick_rows = 5 # How many rows of bricks
active_bricks = []
for row in range(brick_rows):
    for col in range(SCREEN_WIDTH // brick_width):
        brick = Brick(col * brick_width, row * brick_height, brick_width, brick_height)
        active_bricks.append(brick)



# Game loop
running = True
while running:
    screen.fill(BLACK) # Fill screen with background

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    

        

    # Moving paddle
    key_pressed = pygame.key.get_pressed()
    paddle.move(key_pressed)

    # Moving ball
    ball.move()

    # Ball collision with paddle (Only the top)
    if (paddle.x < ball.x < paddle.x + paddle.width and paddle.y < ball.y + ball.radius < paddle.y + paddle.height):
        ball.speed_y *= -1

    
    # Ball collision with bricks (Any part of brick)
    for brick in active_bricks[:]:
        if brick.rect.colliderect(pygame.Rect(ball.x - ball.radius, ball.y - ball.radius, ball.radius * 2, ball.radius * 2)):
            active_bricks.remove(brick)
            ball.speed_y *= -1
            score += 10 # Award 10 points per brick
            break


    # Drawing game objects:
    ball.draw()
    paddle.draw()
    for brick in active_bricks:
        brick.draw()
    


    # Game over condition
    if ball.y >= SCREEN_HEIGHT:
        font = pygame.font.SysFont(None, 74)
        text = font.render("GAME OVER", True, WHITE)
        screen.blit(text, (SCREEN_WIDTH // 2 - 140, SCREEN_HEIGHT // 2))
        pygame.display.flip()
        pygame.time.wait(3000)
        running = False

    # Win condition
    if not active_bricks:
        font = pygame.font.SysFont(None, 74)
        text = font.render("YOU WIN!", True, WHITE)
        screen.blit(text, (SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT // 2))
        pygame.display.flip()
        pygame.time.wait(3000)
        running = False


    # Display the score
    font = pygame.font.SysFont(None, 36)
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, SCREEN_HEIGHT - 40))

    # Update display
    pygame.display.flip()
    clock.tick(60)

# Quit Pygame
pygame.quit()