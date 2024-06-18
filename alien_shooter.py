import game_functions as gf
from pygame.sprite import Group
import pygame
from settings import ArcadeSettings, TimedSettings, SurvivalSettings, Settings
from ship import Ship
from game_stats import GameStats
from button import ArcadeButton, TimeButton, SurvivalButton
from scoreboard import Scoreboard
from timer import Timer

def run_game():
    """Initialize game and create a screen object"""

    # Make objects of the game settings
    game_settings = Settings()
    arcade_settings = ArcadeSettings()
    timed_settings = TimedSettings()
    survival_settings = SurvivalSettings()

    # Initialize the pygame library
    pygame.init()

    # Set screen size and caption
    screen = pygame.display.set_mode((game_settings.screen_width, game_settings.screen_height), pygame.FULLSCREEN)
    pygame.display.set_caption("Alien Shooter")

    # Make the play buttons
    play_arcade = ArcadeButton(screen, "Play Arcade")
    play_time = TimeButton(screen, "Play Timed")
    play_survival = SurvivalButton(screen, "Play Survival")

    # Make an object of ship, group of bullets and aliens
    ship = Ship(game_settings, screen)
    aliens = Group()
    bullets = Group()

    # GameStats and Scoreboard instance
    stats = GameStats(0)
    sb = Scoreboard(game_settings, screen, stats)

    # Create fleet of aliens
    gf.create_fleet(game_settings, screen, ship, aliens)

    # Loop to listen for mode selection after game over
    while True:
        # Check initial mode selection by user
        timer = Timer(game_settings, screen, sb)
        global mode
        mode = gf.check_mouse_down_events(game_settings, arcade_settings, timed_settings, survival_settings, screen, stats, sb, play_arcade, play_time, play_survival, ship,
                                          aliens, bullets, timer)
        # ARCADE MODE
        if mode == 1:
            # Main loop for  running game
            while True and stats.active:
                # Call function to run operations in loop
                game_loop(arcade_settings, screen, stats, sb, play_arcade, play_time, play_survival, ship, aliens, bullets)

            # Call function to store high score
            if stats.score >= stats.high_score:
                stats.save_high_score(stats.score, "arcade_high_score.txt")

        # TIMED MODE
        elif mode == 2:
            # Main loop for  running game
            while True and stats.active:
                # Call function to run operations in loop
                game_loop(timed_settings, screen, stats, sb, play_arcade, play_time, play_survival, ship, aliens, bullets,
                          timer)

                # Check timer value after each pass
                timer.check_timer(stats)

        # SURVIVAL MODE
        elif mode == 3:
            # Main loop for  running game
            while True and stats.active:
                # Call function to run operations in loop
                game_loop(survival_settings, screen, stats, sb, play_arcade, play_time, play_survival, ship, aliens, bullets)

            # Call function to store high score
            if stats.score >= stats.high_score:
                stats.save_high_score(stats.score, "survival_high_score.txt")


def game_loop(game_settings, screen, stats, sb, play_arcade, play_time, play_survival, ship, aliens, bullets, timer=None):
    """Function defining actions in loop of running game"""
    # Listen to events in game
    gf.check_events(game_settings, screen, ship, bullets)

    # Update ship's position on the screen
    ship.update(game_settings)

    # Update bullets position on screen
    gf.update_bullets(game_settings, screen, stats, sb, ship, aliens, bullets)

    # Update aliens position on screen
    gf.update_aliens(game_settings, stats, screen, sb, ship, aliens, bullets)

    # Redraw screen during each pass
    if mode == 2:
        gf.update_screen(game_settings, screen, stats, sb, ship, aliens, bullets, play_arcade, play_time, play_survival, timer)
    else:
        gf.update_screen(game_settings, screen, stats, sb, ship, aliens, bullets, play_arcade, play_time, play_survival)

run_game()