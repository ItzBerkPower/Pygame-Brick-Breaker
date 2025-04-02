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
GRAY = (100, 100, 100)
LIGHT_GRAY = (150,150,150)
ORANGE = (255, 100, 0)
LIGHT_ORANGE = (250,50,0)

levels = {
    1: [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    ],
    2: [
        [1, 1, 1, 1, 2, 1, 1, 1, 1, 2],
        [1, 1, 2, 1, 1, 1, 2, 1, 1, 1],
        [1, 1, 1, 1, 2, 1, 1, 1, 1, 2],
        [1, 2, 1, 1, 1, 2, 1, 1, 1, 1]
    ],
    3: [
        [2, 1, 2, 1, 2, 1, 2, 1, 2, 1],
        [1, 2, 1, 2, 1, 2, 1, 2, 1, 2],
        [2, 1, 2, 1, 2, 1, 2, 1, 2, 1],
        [1, 2, 1, 2, 1, 2, 1, 2, 1, 2],
        [2, 1, 2, 1, 2, 1, 2, 1, 2, 1]
    ],
    4: [
        [1, 3, 1, 1, 2, 1, 1, 3, 1, 1],
        [1, 1, 2, 1, 3, 1, 2, 1, 1, 1],
        [3, 1, 1, 2, 1, 1, 1, 3, 1, 2],
        [1, 2, 1, 1, 3, 1, 2, 1, 1, 1],
        [1, 1, 3, 1, 1, 2, 1, 1, 3, 1]
    ],
    5: [
        [2, 3, 2, 3, 2, 3, 2, 3, 2, 3],
        [3, 2, 3, 2, 3, 2, 3, 2, 3, 2],
        [2, 3, 2, 3, 2, 3, 2, 3, 2, 3],
        [3, 2, 3, 2, 3, 2, 3, 2, 3, 2],
        [2, 3, 2, 3, 2, 3, 2, 3, 2, 3]
    ]
}



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
    def __init__(self, x, y, width, height, brick_type = "normal"):
        super().__init__(x, y, width, height) 
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

        elif self.brick_type == "boss":
            # Boss brick handles its own drawing
            pass




class BossBrick(Brick):  # Now inherits from Brick instead of GameObject
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, "boss")  # Set brick_type to "boss"
        self.health = 10
        self.phase = 1
        self.speed = 2
        self.direction = 1
        self.projectiles = []
        self.last_shot = 0
        self.phase_colors = {
            1: (200, 50, 50),    # Red
            2: (200, 100, 50),   # Orange
            3: (200, 50, 100)    # Purple
        }

    def move(self):
        self.rect.x += self.speed * self.direction
        if self.rect.right >= SCREEN_WIDTH or self.rect.left <= 0:
            self.direction *= -1
            
    def shoot_projectile(self):
        if pygame.time.get_ticks() - self.last_shot > 2000:
            self.last_shot = pygame.time.get_ticks()
            self.projectiles.append(
                Projectile(self.rect.centerx, self.rect.bottom, 0, 5, 5)
            )

    def take_hit(self):
        self.health -= 1
        if self.health == 7:
            self.phase = 2
            self.speed = 3
        elif self.health == 3:
            self.phase = 3
            self.speed = 4

    def draw(self):
        # Override the draw method from Brick
        pygame.draw.rect(screen, self.phase_colors[self.phase], self.rect)
        # Health bar
        health_width = (self.rect.width * self.health) // 10
        pygame.draw.rect(screen, (0, 255, 0), (self.rect.x, self.rect.y - 10, health_width, 5))



class Projectile(GameObject):
    def __init__(self, x, y, radius, speed_x, speed_y):
        super().__init__(x - radius, y - radius, radius * 2, radius * 2)
        self.radius = radius
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.color = (255, 255, 0)  # Yellow projectiles

    def move(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

    def draw(self):
        pygame.draw.circle(screen, self.color, self.rect.center, self.radius)



# AREA FOR FUNCTIONS FOR GAME

# Generating the bricks for a specific level (Initialising brick objects)
def generate_bricks(level):
    if level == 5:  # Boss level
        boss = BossBrick(SCREEN_WIDTH//2 - 100, 50, 200, 40)
        return [boss]
    
    else:
        bricks = []
        level_grid = levels.get(level, levels[1])
        
        for row in range(len(level_grid)):
            for col in range(len(level_grid[row])):

                brick_type_num = level_grid[row][col]

                if brick_type_num == 1:
                    brick_type = "normal"

                elif brick_type_num == 2:
                    brick_type = "indestructible"

                elif brick_type_num == 3:
                    brick_type = "bomb"

                else:
                    continue
                
                brick = Brick(col * brick_width, row * brick_height, brick_width, brick_height, brick_type)
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
                
                if isinstance(brick, BossBrick):
                    brick.take_hit()
                    ball.speed_y *= -1
                    score += 5  # Points per hit
                    
                    # Check if boss is defeated
                    if brick.health <= 0:
                        active_bricks.remove(brick)
                        display_message("BOSS DEFEATED! VICTORY!")
                        return score   
                    
                if brick.brick_type == "normal":
                    active_bricks.remove(brick)
                    score += 10 # Increase score

                    if random.randint(1,8) == 1:
                        powerups.append(PowerUp(brick.rect.centerx, brick.rect.centery))
        
                    ball.speed_y *= -1
                
                # Indestructible blocks, just bounce back
                elif brick.brick_type == "indestructible":
                    ball.speed_y *= -1
            

                if brick.brick_type == "bomb":
                    # Get grid position of bomb
                    bomb_col = brick.rect.x // brick_width
                    bomb_row = brick.rect.y // brick_height
                    
                    # Remove bomb brick
                    active_bricks.remove(brick)
                    score += 20
                    ball.speed_y *= -1
                    
                    # Directions: up, down, left, right
                    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
                    
                    for dr, dc in directions:
                        # Calculate adjacent brick's grid position
                        adj_row, adj_col = bomb_row + dr, bomb_col + dc
                        
                        # Find and remove adjacent brick if it exists
                        for adj_brick in active_bricks[:]:
                            adj_brick_col = adj_brick.rect.x // brick_width
                            adj_brick_row = adj_brick.rect.y // brick_height
                            
                            if (adj_brick_row == adj_row and 
                                adj_brick_col == adj_col and
                                adj_brick.brick_type != "indestructible"):
                                active_bricks.remove(adj_brick)
                                score += 5


    # Handle projectile collisions with paddle
    for brick in active_bricks:
        if isinstance(brick, BossBrick):  # More reliable check than brick_type
            for projectile in brick.projectiles[:]:
                if projectile.check_collision(paddle):
                    brick.projectiles.remove(projectile)
                    # Handle player hit (reduce lives, etc.)
                    display_message("HIT BY BOSS!")
                    # For now, just end game - you might want to add lives system
                    return score


    # Powerup collision with paddle
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

        if isinstance(brick, BossBrick):
            for projectile in brick.projectiles:
                projectile.draw()


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




# Main game function
def main():

    # Initialising ball and paddle objects
    ball = Ball(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, 10, 5 * random.choice([-1, 1]), -5)
    paddle = Paddle((SCREEN_WIDTH - 100) // 2, SCREEN_HEIGHT - 30, 100, 20, 8)

    # Variables:
    score = 0
    powerups = [] # List of power-ups
    balls = [ball] # List of all balls
    current_level = 5
    active_bricks = generate_bricks(current_level)


    # Game loop
    running = True

    while running:
        running = event_handling()


        # Moving all objects
        key_pressed = pygame.key.get_pressed()
        powerups = update_game_objects(paddle, balls, powerups, key_pressed)

        # Update boss and projectiles if in level 5
        if current_level == 5:
            for brick in active_bricks:
                if brick.brick_type == "boss":
                    brick.move()
                    # Shoot projectiles based on phase
                    if brick.phase >= 2:  # Only shoot in phases 2 and 3
                        brick.shoot_projectile()
                    
                    # Update all projectiles
                    for projectile in brick.projectiles[:]:
                        projectile.move()
                        
                        # Remove projectiles that go off-screen
                        if projectile.rect.top > SCREEN_HEIGHT:
                            brick.projectiles.remove(projectile)


        # Check collisions
        score = check_collisions(paddle, balls, active_bricks, powerups, score)

        # Draw game objects
        draw_game_objects(balls, paddle, active_bricks, powerups, score)


        # Game over condition
        if all(ball.rect.bottom >= SCREEN_HEIGHT for ball in balls):
            display_message("GAME OVER")
            running = False


        # Level completed condition
        if not any((brick.brick_type == "normal" or brick.brick_type == "bomb") for brick in active_bricks):
            if current_level < 5:
                display_message(f"Level {current_level} Completed")

                # Moving to next level
                current_level += 1
                active_bricks = generate_bricks(current_level)  # Generate next level bricks
                balls = [Ball(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, 10, 5 * random.choice([-1, 1]), -5)]  # Reset balls
                powerups = []  # Reset power-ups


            # If level 5, just display a "To be continued..." message, as will most likely be a boss fight
            else:
                # Special handling for level 5 (boss level)
                if not any(brick.brick_type == "boss" for brick in active_bricks):
                    display_message("BOSS DEFEATED! YOU WIN!")
                    running = False
                    # Alternatively, you could add a victory screen here
                    # or transition to a new game+ mode with harder bosses


        # Update display
        pygame.display.flip()
        clock.tick(60)


    # Quit Pygame
    pygame.quit()


# Running the game
if __name__ == "__main__":
    main()