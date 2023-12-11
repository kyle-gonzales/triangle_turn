import ast
import socket
import threading
import traceback

from constants import Constants
from game_state import GameState
from triangle import Triangle


class GameServer:
    def __init__(self) -> None:
        self.clients = []

        self.player_data = ""
        self.connected_players_count = 0
        self.game: GameState = GameState()
        # self.game_stage = Constants.WAITING_FOR_PLAYERS

        self.server_socket = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM
        )  # create socket
        self.SERVER_IP = socket.gethostbyname(socket.gethostname())  # get local IP;
        self.ADDRESS = (self.SERVER_IP, Constants.PORT)

        self.server_socket.bind(self.ADDRESS)

        print("SERVER INITIALIZED: Game created successfully...")

    def handle_client(self, client_connection, address):
        is_running = True

        while is_running:
            try:
                message_length = client_connection.recv(Constants.HEADER_SIZE).decode(
                    Constants.FORMAT
                )  # blocks thread until message is received. decode byte stream with UTF-8.

                if not message_length:
                    # stop processing message if message length is invalid
                    return

                message_length = int(message_length)

                message: str = client_connection.recv(message_length).decode(
                    Constants.FORMAT
                )

                if message == Constants.DISCONNECT_MESSAGE:
                    is_running = False
                    self.clients.remove(client_connection)
                    player_id = message.split()[1]
                    self.game.players.pop(player_id)
                    self.game.broadcast(str(self.game))
                    # self.connected_players_count -= 1

                if message.startswith(Constants.TRIANGLE_HEADER):
                    player, square = message.split("&")
                    print(player)
                    print(square)

                    id, angle, triangle_center, color, points = player.split("|")[1:]
                    print("TRIANGLE INFO")
                    print(id)
                    print(angle)
                    print(triangle_center)
                    print(color)
                    print(points)

                    player = self.game.players.get(id)
                    player.angle = angle
                    player.triangle_center = triangle_center
                    player.color = color
                    player.points = points

                    self.game.update(id, player)

                    x, y = square.split("|")[1:]
                    self.game.update_square(x, y)

                    self.broadcast(str(self.game))

                print(f"MESSAGE RECEIVED FROM [{address}]: {message}")

            except Exception as e:
                print(traceback.format_exc())
                raise e

        client_connection.close()
        print(f"SUCCESSFUL DISCONNECTION: {address} has disconnected.")

    def run(self):
        self.server_socket.listen()

        is_running = True

        print(
            f"SERVER IS RUNNING: Server is listening on {self.SERVER_IP} via port {Constants.PORT}\n"
        )

        while is_running:
            client_connection, address = self.server_socket.accept()  # blocks thread

            thread = threading.Thread(
                target=self.handle_client, args=(client_connection, address)
            )

            thread.start()

            self.clients.append(client_connection)

            # print(
            #     f"\nACTIVE CONNECTIONS: {threading.active_count() - 1}"
            # )  # how many threads (clients) are active in this process

    def broadcast(self, package: str):
        for client in self.clients:
            self.send(client, package)

    def send(self, client, package: str):
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

        client.send(header)
        client.send(message)


s = GameServer()
s.run()
