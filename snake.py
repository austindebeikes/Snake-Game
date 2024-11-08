import pygame
import sys
import random

pygame.init()

screen_width, screen_height = 600, 400
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Snake")

BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

snake_size = 20
snake_speed = 10

font = pygame.font.SysFont("Arial", 30)

clock = pygame.time.Clock()

# Initialize snake state
def reset_game():
    global snake_x, snake_y, snake_body, snake_direction, food_x, food_y, score
    snake_x = screen_width // 2
    snake_y = screen_height // 2
    snake_body = [(snake_x, snake_y)]
    snake_direction = "RIGHT"
    food_x = random.randrange(0, screen_width - snake_size, snake_size)
    food_y = random.randrange(0, screen_height - snake_size, snake_size)
    score = 0  # Reset score

def show_start_screen():
    screen.fill(BLACK)
    start_text = font.render("Press any key to start", True, GREEN)
    screen.blit(start_text, (screen_width // 2 - start_text.get_width() // 2, screen_height // 2))
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                waiting = False

def show_game_over_screen():
    screen.fill(BLACK)
    game_over_text = font.render("Game Over! Press any key to restart", True, RED)
    screen.blit(game_over_text, (screen_width // 2 - game_over_text.get_width() // 2, screen_height // 2))
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                waiting = False

# Show start screen once at the beginning
show_start_screen()
reset_game()

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake_direction != "DOWN":
                snake_direction = "UP"
            elif event.key == pygame.K_DOWN and snake_direction != "UP":
                snake_direction = "DOWN"
            elif event.key == pygame.K_LEFT and snake_direction != "RIGHT":
                snake_direction = "LEFT"
            elif event.key == pygame.K_RIGHT and snake_direction != "LEFT":
                snake_direction = "RIGHT"

    # Move snake
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
        show_game_over_screen()
        reset_game()
        show_start_screen()  # Show start screen after reset

    # Check for collisions with itself
    if (snake_x, snake_y) in snake_body:
        show_game_over_screen()
        reset_game()
        show_start_screen()  # Show start screen after reset

    # Update snake body
    snake_body.append((snake_x, snake_y))

    # Check if the snake has eaten the food
    if snake_x == food_x and snake_y == food_y:
        food_x = random.randrange(0, screen_width - snake_size, snake_size)
        food_y = random.randrange(0, screen_height - snake_size, snake_size)
        score += 10  # Increase score
    else:
        snake_body.pop(0)  # Remove tail if no food eaten

    # Draw everything
    screen.fill(BLACK)
    for segment in snake_body:
        pygame.draw.rect(screen, GREEN, (segment[0], segment[1], snake_size, snake_size))
    pygame.draw.rect(screen, RED, (food_x, food_y, snake_size, snake_size))

    # Display score
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (screen_width - score_text.get_width() - 10, 10))

    pygame.display.flip()
    clock.tick(snake_speed)
