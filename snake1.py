import pygame
import sys
import random

pygame.init()

grass_image = pygame.image.load("grass.jpg")

# Screen setup
screen_width, screen_height = 600, 400
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Snake")

# Colors and game variables
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

snake_size = 20
snake_speed = 10

font = pygame.font.SysFont("Arial", 30)
clock = pygame.time.Clock()

# Game state variables
def reset_game():
    global snake_x, snake_y, snake_body, snake_direction, food_x, food_y, score, direction_changed
    snake_x = screen_width // 2
    snake_y = screen_height // 2
    snake_body = [(snake_x, snake_y)]
    snake_direction = "RIGHT"
    food_x = random.randrange(0, screen_width - snake_size, snake_size)
    food_y = random.randrange(0, screen_height - snake_size, snake_size)
    score = 0
    direction_changed = False  # Initialize direction change flag

reset_game()

# Main game loop
while True:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN and not direction_changed:
            # Change direction only if it hasn't already changed this frame
            if event.key == pygame.K_UP and snake_direction != "DOWN":
                snake_direction = "UP"
                direction_changed = True
            elif event.key == pygame.K_DOWN and snake_direction != "UP":
                snake_direction = "DOWN"
                direction_changed = True
            elif event.key == pygame.K_LEFT and snake_direction != "RIGHT":
                snake_direction = "LEFT"
                direction_changed = True
            elif event.key == pygame.K_RIGHT and snake_direction != "LEFT":
                snake_direction = "RIGHT"
                direction_changed = True

    # Move the snake
    if snake_direction == "UP":
        snake_y -= snake_size
    elif snake_direction == "DOWN":
        snake_y += snake_size
    elif snake_direction == "LEFT":
        snake_x -= snake_size
    elif snake_direction == "RIGHT":
        snake_x += snake_size

    # Check for collisions with walls
    if snake_x < 0 or snake_x >= screen_width or snake_y < 0 or snake_y >= screen_height:
        reset_game()

    # Check for collisions with itself
    if (snake_x, snake_y) in snake_body:
        reset_game()

    # Update snake body
    snake_body.append((snake_x, snake_y))

    # Check if the snake has eaten the food
    if snake_x == food_x and snake_y == food_y:
        food_x = random.randrange(0, screen_width - snake_size, snake_size)
        food_y = random.randrange(0, screen_height - snake_size, snake_size)
        score += 10
    else:
        snake_body.pop(0)

    # Draw everything
    screen.blit(grass_image, (0, 0))
    for segment in snake_body:
        pygame.draw.rect(screen, BLACK, (segment[0], segment[1], snake_size, snake_size))
    pygame.draw.rect(screen, RED, (food_x, food_y, snake_size, snake_size))

    # Display score
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    pygame.display.flip()
    clock.tick(snake_speed)

    # Allow direction change again for the next frame
    direction_changed = False
