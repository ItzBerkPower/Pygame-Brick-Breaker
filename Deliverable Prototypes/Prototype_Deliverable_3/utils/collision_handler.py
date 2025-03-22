

def check_collisions(paddle, balls, active_bricks, score):
    for ball in balls:
        if ball.check_collision(paddle):
            ball.speed_y *= -1

        for brick in active_bricks[:]:
            if ball.check_collision(brick):
                active_bricks.remove(brick)
                ball.speed_y *= -1
                score += 10
    return score