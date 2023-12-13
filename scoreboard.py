import pygame

from constants import Constants


class ScoreBoard:
    def __init__(self, players=[]) -> None:
        self.players = players

    def draw(self, screen):
        # Sort players based on points (descending order)
        sorted_players = sorted(self.players, key=lambda x: x.points, reverse=True)

        scoreboard_surface = pygame.Surface((200, 300))  # Adjust size as needed
        scoreboard_surface.set_alpha(128)
        scoreboard_surface.fill((0, 0, 0, 0))  # Background color

        font = pygame.font.Font(None, 24)  # Font for scoreboard text
        for i, player in enumerate(sorted_players):
            text = font.render(
                f"Player {player.id}: {player.points}", True, Constants.WHITE
            )
            text_rect = text.get_rect(x=10, y=30 * i + 10)  # Adjust position as needed
            scoreboard_surface.blit(text, text_rect)
        screen.blit(scoreboard_surface, (10, 10))

