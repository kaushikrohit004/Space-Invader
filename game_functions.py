import sys
import pygame
from bullet import Bullet
from alien import Alien
from time import sleep


def check_events(game_settings, screen, ship, bullets):
    """Respond to events"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, game_settings, screen, ship, bullets)

        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)


def check_mouse_down_events(game_settings, arcade_settings, timed_settings, survival_settings, screen, stats, sb, play_arcade, play_time, play_survival, ship, aliens,
                            bullets, timer):
    """Respond to initial mode selection"""
    # Need to have initial screen drawn
    update_screen(game_settings, screen, stats, sb, ship, aliens, bullets, play_arcade, play_time, play_survival)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if check_play_arcade_button(game_settings, arcade_settings, screen, stats, sb, play_arcade, ship, aliens, bullets,
                                            mouse_x, mouse_y):
                    stats.check_file_present(1)
                    return 1
                if check_play_time_button(game_settings, timed_settings, screen, stats, sb, play_time, ship, aliens, bullets, timer,
                                          mouse_x, mouse_y):
                    return 2
                if check_play_survival_button(game_settings, survival_settings, screen, stats, sb, play_survival, ship, aliens, bullets,
                                              mouse_x, mouse_y):
                    stats.check_file_present(3)
                    update_screen(survival_settings, screen, stats, sb, ship, aliens, bullets, play_arcade, play_time,
                                  play_survival)
                    return 3
            if event.type == pygame.QUIT:
                sys.exit()


def check_keydown_events(event, game_settings, screen, ship, bullets):
    """Check key presses"""
    if event.key == pygame.K_RIGHT:
        # Move ship right
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        # Move ship left
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(game_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()


def check_keyup_events(event, ship):
    """Check key releases"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def check_play_arcade_button(game_settings, arcade_settings, screen, stats, sb, play_arcade, ship, aliens, bullets, mouse_x,
                             mouse_y):
    """Start a new arcade game when the player clicks Play Arcade."""
    button_clicked = play_arcade.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.active:
        # Reset the game settings.
        arcade_settings.initialize_dynamic_settings()

        # Hide the mouse cursor.
        pygame.mouse.set_visible(False)

        # Reset the game statistics.
        stats.reset_stats(arcade_settings.ship_limit)
        stats.active = True

        # Reset high score from file if present
        stats.high_score = stats.check_file_present(1)

        # Reset the scoreboard images.
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()

        # Empty the list of aliens and bullets.
        aliens.empty()
        bullets.empty()

        # Create a new fleet and center the ship.
        create_fleet(arcade_settings, screen, ship, aliens)
        ship.center_ship()
        return True


def check_play_time_button(game_settings, timed_settings, screen, stats, sb, play_time, ship, aliens, bullets, timer, mouse_x,
                           mouse_y):
    """Start a new time game when the player clicks Play Timed."""
    button_clicked = play_time.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.active:
        # Reset the game settings.
        timed_settings.initialize_dynamic_settings()

        # Hide the mouse cursor.
        pygame.mouse.set_visible(False)

        # Reset the game statistics.
        stats.reset_stats(timed_settings.ship_limit)
        stats.active = True

        # Reset high score from file if present
        stats.high_score = stats.check_file_present(2)

        # Reset the scoreboard images.
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()

        # Reset timer
        timer.reset_timer()

        # Empty the list of aliens and bullets.
        aliens.empty()
        bullets.empty()

        # Create a new fleet and center the ship.
        create_fleet(timed_settings, screen, ship, aliens)
        ship.center_ship()
        return True


def check_play_survival_button(game_settings, survival_settings, screen, stats, sb, play_survival, ship, aliens, bullets, mouse_x,
                               mouse_y):
    """Start a new survival game when the player clicks Play Survival."""
    button_clicked = play_survival.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.active:
        # Reset the game settings.
        survival_settings.initialize_dynamic_settings()

        # Hide the mouse cursor.
        pygame.mouse.set_visible(False)

        # Reset the game statistics.
        stats.reset_stats(survival_settings.ship_limit)
        stats.active = True

        # Reset high score from file if present
        stats.high_score = stats.check_file_present(3)

        # Reset the scoreboard images.
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()

        # Empty the list of aliens and bullets.
        aliens.empty()
        bullets.empty()

        # Create a new fleet and center the ship.
        create_fleet(survival_settings, screen, ship, aliens)
        ship.center_ship()
        return True


def fire_bullet(game_settings, screen, ship, bullets):
    """Create a new bullet if limit not reached yet"""
    if len(bullets) < game_settings.bullets_allowed:
        new_bullet = Bullet(game_settings, screen, ship)
        bullets.add(new_bullet)


def update_bullets(game_settings, screen, stats, sb,  ship, aliens, bullets):
    """Update position of bullets and get rid of old bullets"""
    # Update live bullets position on screen (group autocalls for all bullets in sprite)
    bullets.update()

    # Remove old bullets out of the screen space
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    # Check for any bullets hitting aliens
    check_collisions(game_settings, screen, stats, sb, ship, aliens, bullets)


def check_collisions(game_settings, screen, stats, sb,  ship, aliens, bullets):
    """Respond to alien-bullet collisions"""
    # Remove any collided elements
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    # Update scoreboard
    if collisions:
        # Looping through the dictionary values to award points for each alien killed by a bullet
        for aliens in collisions.values():
            stats.score += game_settings.alien_points * len(aliens)
        sb.prep_score()
    check_high_score(stats, sb)

    # No aliens remain
    if len(aliens) == 0:
        # Destroy exisitng bullets and create new fleet
        bullets.empty()
        # Increase game speed after all aliens at a level are destroyed
        game_settings.increase_speed()
        # Increase level
        stats.level += 1
        sb.prep_level()
        # Create fleet after speed increase
        create_fleet(game_settings, screen, ship, aliens)


def create_fleet(game_settings, screen, ship, aliens):
    """Create a full fleet of aliens"""
    # Create an alien and find number of aliens in a row and number of rows
    alien = Alien(game_settings, screen)
    number_aliens_x = get_alien_numbers(game_settings, alien.rect.width)
    number_rows = get_number_rows(game_settings, ship.rect.height, alien.rect.height)

    # Create fleet of aliens
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(game_settings, screen, aliens, alien_number, row_number)


def get_alien_numbers(game_settings, alien_width):
    """Determine number of aliens in a row"""
    available_space_x = game_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


def create_alien(game_settings, screen, aliens, alien_number, row_number):
    """Create alien and place it in row"""
    alien = Alien(game_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)


def get_number_rows(game_settings, ship_height, alien_height):
    """Determine number of rows of aliens to fit on screen"""
    available_space_y = (game_settings.screen_height - (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows


def check_fleet_edges(game_settings, aliens):
    """Respond if aliens have reached an edge"""
    # Change fleet direction if aliens are either at left or right edge
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(game_settings, aliens)
            break


def change_fleet_direction(game_settings, aliens):
    """Drop the entire fleet and change direction"""
    for alien in aliens.sprites():
        alien.rect.y += game_settings.fleet_drop_speed
    game_settings.fleet_direction *= -1


def update_aliens(game_settings, stats, screen, sb, ship, aliens, bullets):
    """Check if fleet is at edge, then update position of all aliens in fleet"""
    check_fleet_edges(game_settings, aliens)
    aliens.update()

    # Look for alien-ship collisions
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(game_settings, stats, screen, sb, ship, aliens, bullets)

    # Look for aliens reaching bottom of screen
    check_aliens_bottom(game_settings, stats, screen, sb, ship, aliens, bullets)


def ship_hit(game_settings, stats, screen, sb, ship, aliens, bullets):
    """Respond to alien-ship hit"""

    if stats.ships_left > 0:
        # Decrement ships left
        stats.ships_left -= 1

        # Update scoreboard
        sb.prep_ships()

        # Empty list of aliens and bullets
        aliens.empty()
        bullets.empty()

        # Create a new fleet and center ship
        create_fleet(game_settings, screen, ship, aliens)
        ship.center_ship()

        # Pause
        sleep(0.5)

        if stats.ships_left == 0:
            stats.active = False
            pygame.mouse.set_visible(True)


def check_aliens_bottom(game_settings, stats, screen, sb, ship, aliens, bullets):
    """Check if any aliens have reached bottom of screen"""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(game_settings, stats, screen, sb, ship, aliens, bullets)
            break


def check_high_score(stats, sb):
    """Check to see if there's a new high score"""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()


def update_screen(game_settings, screen, stats, sb, ship, aliens, bullets, play_arcade, play_time, play_survivial, timer=None):
    """Update images on screen and flip to new screen"""
    screen.fill(game_settings.bg_color)

    if stats.active and timer is not None:
        timer.countdown_timer()

    # Redraw ship and alien
    ship.blitme()

    # draw() works to draw images to screen, to draw shapes user-defined function is needed such as in bullets
    aliens.draw(screen)

    # Redraw all bullets behind ship and aliens
    for bullet in bullets.sprites():
        bullet.draw_bullet()

    # Draw score
    sb.show_score()

    # Draw play buttons only if game is inactive
    if not stats.active:
        play_arcade.draw_button()
        play_time.draw_button()
        play_survivial.draw_button()

    # Make the most recently drawn screen visible
    pygame.display.flip()
