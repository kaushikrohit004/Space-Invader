import pygame
import pygame.font


class Timer:
    """A class to define a timer for timed game"""

    def __init__(self, game_settings, screen, sb):
        """Initialize parameters and frame details"""
        # Used to manage how fast the screen updates
        self.clock = pygame.time.Clock()

        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.game_settings = game_settings
        self.sb = sb
        self.font = pygame.font.SysFont(None, 20)
        self.text_color = (30, 30, 30)

        self.frame_count = 0
        self.frame_rate = 60
        self.start_time = 120

        self.total_seconds = 0

    def reset_timer(self):
        """Reset the timer"""
        self.total_seconds = self.start_time
        self.frame_count = 0

    def countdown_timer(self):
        """Logic for countdown timer"""
        # Calculate total seconds (// is integer division)
        self.total_seconds = self.start_time - (self.frame_count // self.frame_rate)
        if self.total_seconds < 0:
            self.total_seconds = 0

        # Divide by 60 to get total minutes
        minutes = self.total_seconds // 60

        # Use modulus (remainder) to get seconds
        seconds = self.total_seconds % 60

        # Use python string formatting to format in leading zeros
        self.output_string = "Time left: {0:02}:{1:02}".format(minutes, seconds)

        # Call to display timer on screen
        self.prep_timer()

        self.frame_count += 1

        # Limit frames per second
        self.clock.tick(self.frame_rate)

    def prep_timer(self):
        """Show timer on screen"""
        self.timer_image = self.font.render(self.output_string, True, self.text_color, self.game_settings.bg_color)
        # Display the score at the top right of the screen.
        self.timer_rect = self.timer_image.get_rect()
        self.timer_rect.right = self.screen_rect.right - 20
        self.timer_rect.top = self.sb.level_rect.bottom + 10
        self.screen.blit(self.timer_image, self.timer_rect)

    def check_timer(self, stats):
        """Checking timer value at each pass"""
        if self.total_seconds == 0 and stats.active is True:
            # Saving high score to file
            if stats.score >= stats.high_score:
                stats.save_high_score(stats.score, "timed_high_score.txt")

            stats.active = False
            pygame.mouse.set_visible(True)
