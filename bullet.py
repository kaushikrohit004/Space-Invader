import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    """A class to manage bullets fired from the ship"""

    def __init__(self, game_settings, screen, ship):
        """Create a bullet object at the ship's current position"""
        super().__init__()
        self.screen = screen

        # Create a bullet rect at (0,0) and then set correct position
        self.rect = pygame.Rect(0, 0, game_settings.bullet_width, game_settings.bullet_height)
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top

        # Store bullet's position as decimal value
        self.y = float(self.rect.y)

        self.color = game_settings.bullet_color
        self.bullet_speed_factor  = game_settings.bullet_speed_factor

    def update(self):
        """Move bullet up the screen"""
        # Update the decimal position of the bullet
        self.y -= self.bullet_speed_factor
        # Update the rect position
        self.rect.y = self.y

    def draw_bullet(self):
        """Draw bullet on the screen"""
        # Drawing rect of bullet on the screen with color specified from settings.py
        pygame.draw.rect(self.screen, self.color, self.rect)