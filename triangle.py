import math
import random
import sys

import pygame

from constants import Constants


class Triangle:
    def __init__(self) -> None:
        # main triangle components
        self.id = random.randint(1, 100)
        self.angle = 0
        self.triangle_center = (Constants.WIDTH // 2, Constants.HEIGHT // 2)
        self.color = random.choice(Constants.COLORS)
        self.points = 0

        self.is_moving = False

    def get_vertex(self, vertex_number):
        plus_radians = [0, 120, 240]

        return (
            self.triangle_center[0]
            + Constants.TRIANGLE_SIZE
            * math.cos(math.radians(self.angle + plus_radians[vertex_number - 1])),
            self.triangle_center[1]
            + Constants.TRIANGLE_SIZE
            * math.sin(math.radians(self.angle + plus_radians[vertex_number - 1])),
        )

    def draw(self, screen):
        vertex1 = self.get_vertex(1)
        vertex2 = self.get_vertex(2)
        vertex3 = self.get_vertex(3)

        pygame.draw.polygon(screen, self.color, (vertex1, vertex2, vertex3))

        # Calculate the center of the triangle
        center_x = (vertex1[0] + vertex2[0] + vertex3[0]) // 3
        center_y = (vertex1[1] + vertex2[1] + vertex3[1]) // 3

        # Render text (self.id) at the center of the triangle
        font = pygame.font.Font(None, 24)
        text_surface = font.render(f"{self.id} : {self.points}", True, Constants.BLACK)
        text_rect = text_surface.get_rect(center=(center_x, center_y))
        screen.blit(text_surface, text_rect)

    def move(self):
        direction_x = (
            10
            + self.triangle_center[0]
            + Constants.TRIANGLE_SIZE * math.cos(math.radians(self.angle))
        )
        direction_y = (
            10
            + self.triangle_center[1]
            + Constants.TRIANGLE_SIZE * math.sin(math.radians(self.angle))
        )

        # Move towards vertex1
        diff_x = direction_x - self.triangle_center[0]
        diff_y = direction_y - self.triangle_center[1]
        length = math.sqrt(diff_x**2 + diff_y**2)

        if length > 1:
            self.triangle_center = (
                self.triangle_center[0] + diff_x / length,
                self.triangle_center[1] + diff_y / length,
            )

    def spin(self):
        self.angle += Constants.ANGULAR_SPEED

    def __str__(self):
        output = Constants.TRIANGLE_HEADER + "|"
        output += str(self.id) + "|"
        output += str(self.angle) + "|"
        output += str(self.triangle_center) + "|"
        output += str(self.color) + "|"
        output += str(self.points)

        return output
