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
