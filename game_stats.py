import os

class GameStats:
    """Track stats for alien invasion"""

    def __init__(self, ship_limit):
        """Initialize statistics"""
        self.ship_limit = ship_limit
        # Start in an inactive state
        self.active = False
        self.reset_stats(ship_limit)

        self.high_score = 0

    def reset_stats(self, ship_limit):
        """Initialize stats that can change during game"""
        self.ships_left = ship_limit
        self.score = 0
        self.level = 1


    def get_high_score(self, file_name):
        """Get high score from file"""
        try:
            high_score_file = open(file_name, "r")
            self.high_score = int(high_score_file.read())
            high_score_file.close()
            return self.high_score
        except IOError:
            pass
        except ValueError:
            pass

    def save_high_score(self, new_high_score, file_name):
        try:
            """Write high score to file"""
            high_score_file = open(file_name, "w")
            high_score_file.write(str(new_high_score))
            high_score_file.close()
        except IOError:
            pass

    def check_file_present(self, mode):
        """Check if high score files are present and return high score"""
        if os.path.isfile("scores/arcade_high_score.txt") and mode == 1:
            self.high_score = self.get_high_score("scores/arcade_high_score.txt")
            return self.high_score

        if os.path.isfile("scores/timed_high_score.txt") and mode == 2:
            self.high_score = self.get_high_score("scores/timed_high_score.txt")
            return self.high_score

        if os.path.isfile("scores/arcade_high_score.txt") and mode == 3:
            self.high_score = self.get_high_score("scores/survival_high_score.txt")
            return self.high_score

        if not (os.path.isfile("scores/timed_high_score.txt") and os.path.isfile("scores/arcade_high_score.txt") and os.path.isfile(
                "scores/arcade_high_score.txt")):
            self.high_score = 0
            return self.high_score
