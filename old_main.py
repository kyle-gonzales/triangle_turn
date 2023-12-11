import pygame
import sys
import math

import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Set up the display window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Spinning Triangle")

# Triangle constants
triangle_center = (WIDTH // 2, HEIGHT // 2)
triangle_size = 50
angle = 0
angular_speed = 2  # Change this value to adjust rotation speed

# square properties
side_length = 20

# Game loop
running = True
clock = pygame.time.Clock()

def is_collided(head_vertex, rect):
    rect_left = rect[0]
    rect_top = rect[1]
    rect_right = rect[0] + rect[2]
    rect_bottom = rect[1] + rect[3]

    if rect_left <= head_vertex[0] <= rect_right and rect_top <= head_vertex[1] <= rect_bottom:
            return True

    return False

def spawn_square():
    random_x = random.randint(20, WIDTH - side_length - 20)
    random_y = random.randint(20, HEIGHT - side_length - 20)

    return random_x, random_y




while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                moving = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                moving = False

    # Update
    if moving:
        # Calculate direction to vertex1
        direction_x = triangle_center[0] + triangle_size * math.cos(math.radians(angle))
        direction_y = triangle_center[1] + triangle_size * math.sin(math.radians(angle))

        # Move towards vertex1
        diff_x = direction_x - triangle_center[0]
        diff_y = direction_y - triangle_center[1]
        length = math.sqrt(diff_x**2 + diff_y**2)

        if length > 1:
            triangle_center = (
                triangle_center[0] + diff_x / length,
                triangle_center[1] + diff_y / length
            )
        else:
            moving = False  # Stop moving when reached vertex1

    # Increment angle for rotation
    if not moving:
        angle += angular_speed

    # Draw / Render
    screen.fill(BLACK)

    # Calculate triangle vertices
    vertex1 = (
        triangle_center[0] + triangle_size * math.cos(math.radians(angle)),
        triangle_center[1] + triangle_size * math.sin(math.radians(angle))
    )
    vertex2 = (
        triangle_center[0] + triangle_size * math.cos(math.radians(angle + 120)),
        triangle_center[1] + triangle_size * math.sin(math.radians(angle + 120))
    )
    vertex3 = (
        triangle_center[0] + triangle_size * math.cos(math.radians(angle + 240)),
        triangle_center[1] + triangle_size * math.sin(math.radians(angle + 240))
    )

    pygame.draw.rect(screen, (0,255,0), (x, y, side_length, side_length, ))
    if is_collided(vertex1, (x,y,side_length,side_length)):
        x,y = spawn_square()


    # Draw the triangle
    pygame.draw.polygon(screen, RED, (vertex1, vertex2, vertex3))


    # Update the display
    pygame.display.flip()

    # Control frame rate
    clock.tick(FPS)

# Quit Pygame
pygame.quit()
sys.exit()
