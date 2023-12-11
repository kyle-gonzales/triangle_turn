import pygame
import sys
import math

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
pygame.display.set_caption("Isosceles Triangle Movement")

# Triangle properties
triangle_center = (WIDTH // 2, HEIGHT // 2)
equal_side_length = 150
smaller_side_length = 100
angle = 0
angular_speed = 2
moving = False

# Game loop
running = True
clock = pygame.time.Clock()

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
        # Calculate direction towards the vertex connecting the two equal sides
        direction_x = triangle_center[0] + equal_side_length * math.cos(math.radians(angle + 90))
        direction_y = triangle_center[1] + equal_side_length * math.sin(math.radians(angle + 90))

        # Move towards the vertex
        diff_x = direction_x - triangle_center[0]
        diff_y = direction_y - triangle_center[1]
        length = math.sqrt(diff_x**2 + diff_y**2)

        if length > 1:
            triangle_center = (
                triangle_center[0] + diff_x / length,
                triangle_center[1] + diff_y / length
            )
        else:
            moving = False  # Stop moving when reached the vertex

    # Increment angle for rotation
    if not moving:
        angle += angular_speed

    # Draw / Render
    screen.fill(BLACK)

    # Calculate triangle vertices
    vertex1 = (
        triangle_center[0] + equal_side_length * math.cos(math.radians(angle)),
        triangle_center[1] + equal_side_length * math.sin(math.radians(angle))
    )
    vertex2 = (
        triangle_center[0] + equal_side_length * math.cos(math.radians(angle + 120)),
        triangle_center[1] + equal_side_length * math.sin(math.radians(angle + 120))
    )
    vertex3 = (
        triangle_center[0] + smaller_side_length * math.cos(math.radians(angle + 60)),
        triangle_center[1] + smaller_side_length * math.sin(math.radians(angle + 60))
    )

    # Draw the triangle
    pygame.draw.polygon(screen, RED, (vertex1, vertex2, vertex3))

    # Update the display
    pygame.display.flip()

    # Control frame rate
    clock.tick(FPS)

# Quit Pygame
pygame.quit()
sys.exit()
