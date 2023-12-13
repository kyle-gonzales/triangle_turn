import ast
import socket
import sys
import threading
import time

import pygame

from constants import Constants
from scoreboard import ScoreBoard
from square import Square
from triangle import Triangle
from serverinput import InputServer

# Initialize Pygame
pygame.init()

# Set up the display window
SCREEN = pygame.display.set_mode((Constants.WIDTH, Constants.HEIGHT))
pygame.display.set_caption(Constants.APP_NAME)


class Client:


    def __init__(self) -> None:
        self.server = ""  # paste the IP of the server here
        self.ip = "172.16.3.189"

        self.running = False
        self.server_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.SERVER_ADDRESS = [self.server, Constants.PORT]
        self.triangle = Triangle()

        self.other_triangles = []
        self.square = None
        self.hit_flag = False

    def connect(self):
        self.SERVER_ADDRESS = [self.server, Constants.PORT]
        self.server_connection.connect(tuple(self.SERVER_ADDRESS))
        self.server_connection.settimeout(0.05)
        self.send(f"CONNECT {self.triangle.id}")

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

    def handle_messages(self):
        while self.running:
            message = ""

            try:
                message = self.receive_message()
            except Exception as e:
                # print(e)
                pass

            if message.startswith(Constants.SQUARE_HEADER):
                x, y = message.split("|")[1:]
                self.square.x = ast.literal_eval(x)
                self.square.y = ast.literal_eval(y)

            elif message.startswith(Constants.TRIANGLE_HEADER):
                players, square = message.split("&")
                players = players.split(";")

                for p in players:
                    id, angle, triangle_center, color, points = p.split("|")[1:]

                    if id == self.triangle.id:
                        self.triangle.angle = ast.literal_eval(angle)
                        self.triangle.triangle_center = ast.literal_eval(
                            triangle_center
                        )
                        self.triangle.color = ast.literal_eval(color)
                        self.triangle.points = ast.literal_eval(points)
                    else:
                        player = Triangle()
                        player.id = ast.literal_eval(id)
                        player.angle = ast.literal_eval(angle)
                        player.triangle_center = ast.literal_eval(triangle_center)
                        player.color = ast.literal_eval(color)
                        player.points = ast.literal_eval(points)

                        self.other_triangles.append(player)

                x, y = square.split("|")[1:]
                self.square.x = ast.literal_eval(x)
                self.square.y = ast.literal_eval(y)

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

        # print(f"RECEIVED FROM SERVER: {message}")
        return message

    def main(self):
        self.running = True
        # server_input = InputServer()

        # Start a separate thread for receiving messages
        receive_thread = threading.Thread(target=self.handle_messages)
        receive_thread.start()

        clock = pygame.time.Clock()

        while self.running:
            # Event handling

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.send(
                        Constants.DISCONNECT_MESSAGE + " " + str(self.triangle.id)
                    )
                    self.running = False

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

            if self.square.is_hit(self.triangle.get_vertex(1)):
                if not self.hit_flag:
                    self.send(f"HIT {time.time()}")
                    # self.square.spawn_square()
                    self.triangle.points += 1
                    print(f"{self.triangle.id} = {self.triangle.points}")
            else:
                self.hit_flag = False

            try:
                # self.send(str(self.triangle) + "&" + str(self.square))
                self.send(str(self.triangle))
            except (
                Exception
            ) as e:  #! be careful if you notice that message is not being sent
                # print(e)
                pass

            SCREEN.fill(Constants.BLACK)  # change background here

            self.square.draw(SCREEN)
            for t in self.other_triangles:
                t.draw(SCREEN)
            self.other_triangles.clear()
            self.triangle.draw(SCREEN)

            # scoreboard = ScoreBoard(self.other_triangles)
            # scoreboard.players.append(self.triangle)
            # scoreboard.draw(SCREEN)

            # Update the display
            pygame.display.flip()

            # Control frame rate
            clock.tick(Constants.FPS)

        # Quit Pygame
        pygame.quit()
        sys.exit()

    def connect_window(self):
        clock = pygame.time.Clock()
        running = True

        large_font = pygame.font.Font(None, 60)
        small_font = pygame.font.Font(None, 36)

        while running:
            message = ""

            try:
                message = self.receive_message()
            except Exception as e:
                # print(e)
                pass

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                # if event.type == pygame.MOUSEBUTTONDOWN:
                #     if event.button == 1:
                #         self.connect()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        # self.server = server_input.enter_server()
                        try:
                            self.server = self.server.strip()
                            print(self.server)
                            self.connect()
                        except Exception as e:
                            print(e)
                            print("failed to connect")
                    elif event.key == pygame.K_BACKSPACE:
                        self.server = self.server[:-1]
                    else:
                        self.server += event.unicode

            if message.startswith(Constants.SQUARE_HEADER):
                # receiving square coordinates from the server indicates a successful connection. we may go to the main screen.
                x, y = message.split("|")[1:]
                self.square = Square()
                self.square.x = ast.literal_eval(x)
                self.square.y = ast.literal_eval(y)
                self.main()

            SCREEN.fill(Constants.BLACK)  # change background here

            title_text = large_font.render(Constants.APP_NAME, True, Constants.WHITE)
            title_rect = title_text.get_rect(center=SCREEN.get_rect().center)

            SCREEN.blit(title_text, title_rect)

            click_to_start_text = small_font.render(
                "Press ENTER to Start...", True, Constants.WHITE
            )  # Change color if needed
            click_to_start_rect = click_to_start_text.get_rect()
            click_to_start_rect.midbottom = (Constants.WIDTH / 2, Constants.HEIGHT - 50)
            SCREEN.blit(click_to_start_text, click_to_start_rect)
            SCREEN.blit(
                click_to_start_text,
                click_to_start_rect,
            )

            server_text = small_font.render(
                "Enter Server IP: " + self.server, True, Constants.WHITE
            )  # Change color if needed
            server_rect = server_text.get_rect()
            server_rect.midbottom = (Constants.WIDTH / 2, Constants.HEIGHT - 100)
            SCREEN.blit(server_text, server_rect)
            SCREEN.blit(
                server_text,
                server_rect,
            )

            # Update the display
            pygame.display.flip()

            # Control frame rate
            clock.tick(Constants.FPS)


c = Client()
c.connect_window()
