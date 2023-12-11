from square import Square
from triangle import Triangle

"""
player information serialization:

PLAYER id x;PLAYER id x
"""


class GameState:
    players = dict()  # player_name/id (string): player_instance (Player)
    square = Square()

    def update_square(self, x, y):
        self.square.x = x
        self.square.y = y

    def update(self, name: str, player: Triangle):
        self.players[player.id] = player

    def __str__(self) -> str:
        output = ""

        for name, player in self.players.items():
            output += str(player) + ";"

        return f"{output[:-1]}&{self.square}"
