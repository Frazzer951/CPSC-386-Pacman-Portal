from vector import Vector


class Settings:
    """A class to store all settings for Alien Invasion."""

    def __init__(self):
        """Initialize the game's settings."""
        # Screen settings
        self.screen_width = 650
        self.screen_height = 800
        self.bg_color = (0, 0, 0)

        # Pacman settings
        self.pacman_start = Vector(12, 22)

        # Ghost settings
        self.blinky_start = Vector(11, 13)
        self.inky_start = Vector(12, 13)
        self.pinky_start = Vector(13, 13)
        self.clyde_start = Vector(14, 13)

        # Points
        self.point_orb_score = 10
        self.power_up_score = 50
        self.fruit_score = 100
