import pygame.font
from button import Button
from pygame.sprite import Group


class TeamScoreboard:
    """A class to display scoring information."""

    def __init__(self, quiz, team):
        """Initialize scorekeeping attributes."""
        self.quiz = quiz
        self.screen = quiz.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = quiz.settings
        self.team = team

        # Font for scoring information
        self.text_color = self.team.text_color
        self.bg_color = self.team.bg_color
        self.font = pygame.font.SysFont(None, 48)
        self.player_font = pygame.font.SysFont(None, 36)
        self.buzzer_font = pygame.font.SysFont(None, 24)

        # Prepare the inital score image
        self.prep_score()
        self.prep_player_scores()
        self.prep_player_buzzers()
        self.prep_add_players()

    def prep_score(self):
        """Turn score into an image."""
        rounded_score = round(self.team.score, 0)
        score_str = f"{self.team.name}: {rounded_score}"
        self.score_image = self.font.render(score_str, True, self.text_color, self.bg_color)

        # Display the score in the center on the correct side
        self.score_rect = self.score_image.get_rect()
        self.score_rect.top = self.screen_rect.top + 60
        if self.team.display_side == 'right':
            self.score_rect.right = self.screen_rect.right - 20
        else:
            self.score_rect.left = self.screen_rect.left + 20
        self.bottom_rect = self.score_rect

    def prep_player_scores(self):
        """Turn member scores into an image."""
        self.player_score_rects = []
        self.player_score_images = []
        for player in self.team.players:
            player_score = round(player.score, 0)
            player_score_str = f"{player.name}: {player_score}"
            player_score_image = self.player_font.render(player_score_str, True, self.text_color, self.settings.bg_color)
            self.player_score_images.append(player_score_image)

            # Display the under the team score
            if self.player_score_rects:
                above_rect = self.player_score_rects[-1]
            else:
                above_rect = self.score_rect
            player_score_rect = player_score_image.get_rect()
            if self.team.display_side == 'right':
                player_score_rect.right = above_rect.right
            else:
                player_score_rect.left = above_rect.left
            player_score_rect.top = above_rect.bottom
            self.player_score_rects.append(player_score_rect)
            self.bottom_rect = player_score_rect

    def prep_player_buzzers(self):
        """Add buzzers to player names."""
        self.buzzer_rects = []
        self.buzzer_images = []
        for rect in self.player_score_rects:
            buzzer_image = self.buzzer_font.render('Buzz', True, self.text_color, self.settings.bg_color)
            self.buzzer_images.append(buzzer_image)

            # Display next to the player name
            buzzer_rect = buzzer_image.get_rect()
            if self.team.display_side == 'right':
                buzzer_rect.right = rect.left - 20
            else:
                buzzer_rect.left = rect.right + 20
            buzzer_rect.centery = rect.centery
            self.buzzer_rects.append(buzzer_rect)

    def prep_add_players(self):
        self.add_button = Button(self, beneath=self.bottom_rect, msg='Add Player')

    def check_buzz(self, mouse_pos):
        """Checks if any of the player buzz buttons have been pressed."""
        for i, rect in enumerate(self.buzzer_rects):
            if rect.collidepoint(mouse_pos):
                return self.team.players[i]

    def show_score(self):
        """Draw score and ships to the screen."""
        self.prep_score()
        self.prep_player_scores()
        self.prep_player_buzzers()
        self.prep_add_players()

        if not self.quiz.game_active:
            self.add_button.draw_button()

        self.screen.blit(self.score_image, self.score_rect)
        for i, image in enumerate(self.player_score_images):
            self.screen.blit(image, self.player_score_rects[i])
            if self.quiz.game_active:
                self.screen.blit(self.buzzer_images[i], self.buzzer_rects[i])

