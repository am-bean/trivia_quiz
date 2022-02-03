from player import Player
from question import Question
from button import Button
from team import Team
from scoreboard import TeamScoreboard
import pandas as pd
from settings import Settings
import pygame
import random
import sys
from time import sleep


class Quiz:

    def __init__(self):

        # Setup pygame
        self.settings = Settings()
        pygame.init()
        pygame.display.set_caption("Trivia Quiz")
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        self.screen_rect = self.screen.get_rect()

        self.players = []
        self.questions = []
        self.teams = [Team(self, 'Red'), Team(self, 'Blue')]
        self._load_questions()
        self.current_question = self.questions[0]

        self.play_button = Button(self, 'Start Quiz')
        self.scoreboards = [TeamScoreboard(self, self.teams[0]), TeamScoreboard(self, self.teams[1])]
        self.game_active = False
        self.pause_question = False

        self.text_input_mode = False
        self.add_player_mode = False
        self.submit_answer_mode = False
        self.correct_answer = False
        self.display_answer = False
        self.user_text = ''

    def _load_questions(self):
        file = 'questions.xlsx'
        questions = pd.read_excel(file, header=0, usecols='A:C')
        self.questions = [Question(self, row['prompt'], row['answer'], row['category']) for i, row in
                          questions.iterrows()]
        random.shuffle(self.questions)

    def _update_screen(self):
        """Refresh the screen with new images."""
        # Redraw the screen.
        self.screen.fill(self.settings.bg_color)

        for sb in self.scoreboards:
            sb.show_score()

        # Draw buttons if the game is inactive
        if not self.game_active:
            self.play_button.draw_button()
        else:
            self.current_question.display_question()

        if self.text_input_mode:
            self._draw_user_text()

        if self.submit_answer_mode:
            self._draw_user_text()

        if self.display_answer:
            self.current_question.display_answer()

        # Make the most recently drawn screen visible.
        pygame.display.flip()

    def _check_events(self):
        """Respond to keypresses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
            elif event.type == pygame.KEYDOWN and not self.text_input_mode:
                self._check_keydown_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN and not self.text_input_mode:
                mouse_pos = pygame.mouse.get_pos()
                self._check_mouse_click(mouse_pos)
            elif event.type == pygame.KEYDOWN and self.text_input_mode:
                self._collect_keydown_info(event)

    def _check_mouse_click(self, mouse_pos):
        """Respond to various click locations."""
        if self.play_button.rect.collidepoint(mouse_pos) and not self.game_active:
            self.game_active = True
        elif self.scoreboards[0].add_button.rect.collidepoint(mouse_pos) and not self.game_active:
            self.text_input_mode = True
            self.add_player_mode = True
            self.add_to_team = self.teams[0]
        elif self.scoreboards[1].add_button.rect.collidepoint(mouse_pos) and not self.game_active:
            self.text_input_mode = True
            self.add_player_mode = True
            self.add_to_team = self.teams[1]
        elif self.game_active:
            self.buzz_player = self.scoreboards[0].check_buzz(mouse_pos)
            if self.buzz_player:
                self.text_input_mode = True
                self.submit_answer_mode = True
            else:
                self.buzz_player = self.scoreboards[1].check_buzz(mouse_pos)
                if self.buzz_player:
                    self.text_input_mode = True
                    self.submit_answer_mode = True

    def _check_keydown_events(self, event):
        """Responds to keydown events."""
        if event.key == pygame.K_SPACE:
            # Pause the question
            self.pause_question = not self.pause_question

    def _collect_keydown_info(self, event):
        """Responds to keydown events in text entry mode."""
        if event.key == pygame.K_RETURN:
            if self.add_player_mode:
                self.text_input_mode = False
                self.add_player_mode = False
                if self.user_text:
                    new_player = Player(self.user_text)
                    self.players.append(new_player)
                    self.add_to_team.add_player(new_player)
                self.user_text = ''
            if self.submit_answer_mode:
                self.text_input_mode = False
                self.submit_answer_mode = False
                self.correct_answer = self.current_question.check_answer(self.user_text)
                self.user_text = ''
                if self.correct_answer:
                    self.buzz_player.score_points(self.settings.correct_score)
                    self.display_answer = True
                else:
                    self.buzz_player.score_points(self.settings.incorrect_score)
                    self.display_answer = True
        elif event.key == pygame.K_BACKSPACE:
            self.user_text = self.user_text[:-1]
        else:
            self.user_text += event.unicode

    def _draw_user_text(self):
        font = pygame.font.SysFont(None, 36)
        # Text input box
        self.user_text_image = font.render(self.user_text, True, (0, 0, 0), self.settings.bg_color)
        self.text_input_rect = self.user_text_image.get_rect()
        self.text_input_rect.centerx = self.screen_rect.centerx
        self.text_input_rect.bottom = self.screen_rect.bottom

        # Label box
        if self.add_player_mode:
            label_text = 'Adding Player:'
        elif self.submit_answer_mode:
            label_text = f'Buzz from {self.buzz_player.name}. What is your answer?'
        self.user_text_label_image = font.render(label_text, True, (0, 0, 0), self.settings.bg_color)
        self.text_input_label_rect = self.user_text_label_image.get_rect()
        self.text_input_label_rect.centerx = self.screen_rect.centerx
        self.text_input_label_rect.bottom = self.text_input_rect.top - 10

        self.screen.blit(self.user_text_image, self.text_input_rect)
        self.screen.blit(self.user_text_label_image, self.text_input_label_rect)

    def run_quiz(self):
        while True:
            self._check_events()
            self._update_screen()


if __name__ == "__main__":
    # Make game instance and run the game.
    q = Quiz()
    q.run_quiz()
