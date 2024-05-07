import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Screen dimensions and settings
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
RED = (200, 0, 0)
BLUE = (0, 0, 200)
GOLD = (255, 215, 0)
GREEN = (0, 255, 0)
SKY_BLUE = (135, 206, 235)

# Bird settings
GRAVITY = 0.25
BIRD_FLAP_POWER = 7
GAME_SPEED = 5

# Setup the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Ottoman Flappy Bird")

# Clock
clock = pygame.time.Clock()

# Load fonts
font = pygame.font.SysFont('Arial', 28, bold=True)

# Function to draw the bird
def draw_bird(screen, x, y):
    pygame.draw.ellipse(screen, GOLD, (x, y, 34, 24))  # Body
    pygame.draw.circle(screen, RED, (x + 24, y + 12), 8)  # Head
    pygame.draw.polygon(screen, BLUE, [(x + 34, y + 12), (x + 44, y + 8), (x + 34, y + 16)])  # Beak

# Function to draw the pipes
def draw_pipes(screen, pipes):
    for pipe in pipes:
        pygame.draw.rect(screen, GREEN, pipe)

# Function to create a new pair of pipes
def create_pipe():
    offset = random.randrange(150, 350)
    bottom_pipe = pygame.Rect(SCREEN_WIDTH, SCREEN_HEIGHT - offset, 50, offset)
    top_pipe = pygame.Rect(SCREEN_WIDTH, 0, 50, SCREEN_HEIGHT - offset - 200)
    return bottom_pipe, top_pipe

# Check for collisions
def check_collision(pipes, bird_rect):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            return False
    if bird_rect.top <= -50 or bird_rect.bottom >= 550:
        return False
    return True

# Move the pipes to the left
def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= GAME_SPEED
    return [pipe for pipe in pipes if pipe.right > 0]

# Draw the score on the screen
def draw_score(screen, score):
    score_surface = font.render(str(score), True, WHITE)
    score_rect = score_surface.get_rect(center=(SCREEN_WIDTH // 2, 50))
    screen.blit(score_surface, score_rect)

# Check and update the score
def score_check(pipes):
    global score
    for pipe in pipes:
        if 95 < pipe.centerx < 105:
            score += 1

# Game variables
bird_x, bird_y = 60, 150
bird_movement = 0
pipes = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1200)
score = 0

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird_movement = 0
                bird_movement -= BIRD_FLAP_POWER
        if event.type == SPAWNPIPE:
            pipes.extend(create_pipe())

    # Fill the screen with a sky blue color
    screen.fill(SKY_BLUE)

    # Bird
    bird_movement += GRAVITY
    bird_y += bird_movement
    bird_rect = pygame.Rect(bird_x, bird_y, 34, 24)
    draw_bird(screen, bird_x, bird_y)

    # Pipes
    pipes = move_pipes(pipes)
    draw_pipes(screen, pipes)

    # Base (ground)
    pygame.draw.rect(screen, WHITE, (0, 550, SCREEN_WIDTH, 50))

    # Score
    score_check(pipes)
    draw_score(screen, score)

    # Check for collisions
    if not check_collision(pipes, bird_rect):
        running = False

    # Update the display
    pygame.display.update()
    clock.tick(FPS)