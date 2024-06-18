import pygame
from pygame.sprite import Sprite


class Ship(Sprite):

    def __init__(self, game_settings, screen):
        """Initialize the ship and set its starting position"""
        super().__init__()
        self.screen = screen
        self.moving_right = False
        self.moving_left = False
        self.game_settings = game_settings

        # Load ship image and get its rect (rectangle coordinates)
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()

        # Get screen rectangle coordinates
        self.screen_rect = screen.get_rect()

        # Start each new ship at the bottom of the screen
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        # Store decimal value for ship's centre
        self.center = float(self.rect.centerx)

    def blitme(self):
        """Draw the ship at its current location"""
        self.screen.blit(self.image, self.rect)

    def update(self, game_settings):
        """Update the ship's position based on movement flags"""
        # Update ship's center value, not rect
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += game_settings.ship_speed_factor
        elif self.moving_left and self.rect.left > 0:
            self.center -= game_settings.ship_speed_factor

        # Update rect object from self.center (stores integer values)
        self.rect.centerx = self.center

    def center_ship(self):
        """Center ship to screen"""
        # Ship's center is equated to screen center thru rect coordinates
        self.center = self.screen_rect.centerx