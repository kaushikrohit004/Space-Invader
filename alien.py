import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    """Class to represent single alien in the fleet"""

    def __init__(self, game_settings, screen):
        """Initialize alien and set starting position"""
        super().__init__()
        self.screen = screen
        self.game_settings = game_settings

        # Load alien image and get rect attribute
        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()

        # Start each alien over top left of the screen
        # Then add padding equal to its width and height
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store alien's exact position
        self.x = float(self.rect.x)

    def blitme(self):
        """Draw the alien at its current location"""
        self.screen.blit(self.image, self.rect)

    def update(self):
        """Move the alien right or left"""
        self.x += (self.game_settings.alien_speed_factor * self.game_settings.fleet_direction)
        self.rect.x = self.x

    def check_edges(self):
        """Return true if alien is at edge of screen"""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True
