import ast
import math
import random
import socket
import sys

import pygame

from constants import Constants
from square import Square
from triangle import Triangle

# Initialize Pygame
pygame.init()

# Set up the display window
SCREEN = pygame.display.set_mode((Constants.WIDTH, Constants.HEIGHT))
pygame.display.set_caption(Constants.APP_NAME)


# TODO CLEANLY DISCONNECT FROM GAME
class Client:
    server = "192.168.1.25"  # paste the IP of the server here

    def __init__(self) -> None:
        self.server_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.SERVER_ADDRESS = (self.server, Constants.PORT)
        self.triangle = Triangle()
        self.server_connection.connect(self.SERVER_ADDRESS)
        self.server_connection.settimeout(0.05)
        self.send(f"player {self.triangle.id} connected")

    def send(self, package: str):
        message = package.encode(
            Constants.FORMAT
        )  # encode the string into a byte stream

        message_length = len(message)

        header = str(message_length).encode(
            Constants.FORMAT
        )  # the initial header to send to the server

        header += b" " * (
            Constants.HEADER_SIZE - len(header)
        )  # pad the header with the byte representation of a whitespace to ensure that the header is 64 bytes long

        self.server_connection.send(header)
        self.server_connection.send(message)

    def receive_message(self):
        message_length = self.server_connection.recv(Constants.HEADER_SIZE).decode(
            Constants.FORMAT
        )  # blocks thread until message is received. decode byte stream with UTF-8.

        if not message_length:
            # stop processing message if message length is invalid
            return

        message_length = int(message_length)

        message: str = self.server_connection.recv(message_length).decode(
            Constants.FORMAT
        )

        print(f"RECEIVED FROM SERVER: {message}")
        return message

    def main(self):
        running = True
        clock = pygame.time.Clock()

        square = Square()

        while running:
            # Event handling

            message = ""
            triangles = []

            try:
                message = self.receive_message()
            except Exception as e:
                # print(e)
                pass

            if message.startswith(Constants.TRIANGLE_HEADER):
                players, square = message.split("&")
                print(players)
                print(square)
                players = players.split(";")
                print(players)

                for p in players:
                    id, angle, triangle_center, color, points = p.split("|")[1:]

                    if id == self.triangle.id:
                        self.triangle.angle = angle
                        self.triangle.triangle_center = triangle_center
                        self.triangle.color = color
                        self.triangle.points = points
                    else:
                        player = Triangle()
                        player.angle = ast.literal_eval(angle)
                        player.triangle_center = ast.literal_eval(triangle_center)
                        player.color = ast.literal_eval(color)
                        player.points = ast.literal_eval(points)

                        triangles.append(player)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.send(
                        Constants.DISCONNECT_MESSAGE + " " + str(self.triangle.id)
                    )
                    running = False

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.triangle.is_moving = True
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_SPACE:
                        self.triangle.is_moving = False

            if self.triangle.is_moving:
                self.triangle.move()
            else:
                self.triangle.spin()

            try:
                self.send(str(self.triangle) + "&" + str(square))
                print("sent")

                # send square position
                # send updated client position

            except (
                Exception
            ) as e:  #! be careful if you notice that message is not being sent
                print(e)
                pass

            SCREEN.fill(Constants.BLACK)

            if square.is_hit(self.triangle.get_vertex(1)):
                square.spawn_square()
                self.triangle.points += 1
                print(f"{self.triangle.id} = {self.triangle.points}")

            square.draw(SCREEN)
            for t in triangles:
                t.draw(SCREEN)
            self.triangle.draw(SCREEN)

            # Update the display
            pygame.display.flip()

            # Control frame rate
            clock.tick(Constants.FPS)

        # Quit Pygame
        pygame.quit()
        sys.exit()


c = Client()
c.main()
