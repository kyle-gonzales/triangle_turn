import random

import pygame

from constants import Constants


class Square:
    def __init__(self) -> None:
        self.x = 100
        self.y = 100

    def spawn_square(self):
        random_x = random.randint(20, Constants.WIDTH - Constants.SIDE_LENGTH - 20)
        random_y = random.randint(20, Constants.HEIGHT - Constants.SIDE_LENGTH - 20)

        self.x, self.y = random_x, random_y

    def is_hit(self, head_vertex):
        rect_left = self.x
        rect_top = self.y
        rect_right = self.x + Constants.SIDE_LENGTH
        rect_bottom = self.y + Constants.SIDE_LENGTH

        if (
            rect_left <= head_vertex[0] <= rect_right
            and rect_top <= head_vertex[1] <= rect_bottom
        ):
            return True

    def draw(self, screen):
        pygame.draw.rect(
            screen,
            (0, 255, 0),
            (self.x, self.y, Constants.SIDE_LENGTH, Constants.SIDE_LENGTH),
        )

    def __str__(self) -> str:
        output = Constants.SQUARE_HEADER + "|"

        output += str(self.x) + "|"
        output += str(self.y)

        return output
