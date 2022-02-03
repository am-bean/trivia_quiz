class Settings:
    """A class to store all the settings."""

    def __init__(self):
        """Initialize the game's static settings."""
        self.correct_score = 10
        self.incorrect_score = -5

        self.screen_width = 1200
        self.screen_height = 600
        self.bg_color = (230, 230, 230)  # light gray
        self.fullscreen = False

        # Team Formatting
        self.colors = {'Red': (255, 51, 51), 'Blue': (51, 51, 255)}
        self.sides = {'Red': 'right', 'Blue': 'left'}

        #Button Formatting
        self.button_font_size = {'Start Quiz': 48, 'Add Player': 24}

