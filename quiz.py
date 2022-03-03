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
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height), pygame.FULLSCREEN)
        self.screen_rect = self.screen.get_rect()

        self.players = []
        self.questions = []
        self.teams = [Team(self, 'Red'), Team(self, 'Blue')]
        self._load_questions()
        self.current_question_index = 0
        self.current_question = self.questions[self.current_question_index]

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

        self._draw_header()

        for sb in self.scoreboards:
            sb.show_score()

        # Draw buttons if the game is inactive
        if not self.game_active:
            self.play_button.draw_button()
        else:
            self.current_question.display_question()
            self._draw_next_button()
            self._show_answer()

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
            if self.next_image_rect.collidepoint(mouse_pos):
                self.current_question_index += 1
                self.current_question = self.questions[self.current_question_index]
                self.display_answer = False
            if self.show_answer_rect.collidepoint(mouse_pos):
                self.display_answer = not self.display_answer

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

    def _draw_header(self):
        font = pygame.font.SysFont('Courgette', 36)
        # Label box
        self.title_image = font.render('Blackfriars Trivia', True, (0, 0, 0), self.settings.bg_color)
        self.title_image_rect = self.title_image.get_rect()
        self.title_image_rect.centerx = self.screen_rect.centerx
        self.title_image_rect.top = self.screen_rect.top + 20

        self.screen.blit(self.title_image, self.title_image_rect)
        arms = pygame.image.load('Blackfriars_Arms.png')
        arms = pygame.transform.scale(arms, (50, 60))
        arms_rect = arms.get_rect()
        arms_rect.centerx = self.title_image_rect.centerx
        arms_rect.top = self.title_image_rect.bottom
        self.screen.blit(arms, arms_rect)

    def _draw_next_button(self):
        font = pygame.font.SysFont(None, 36)
        # Label box
        self.next_image = font.render('Next', True, (0, 0, 0), (110, 210, 230))
        self.next_image_rect = self.next_image.get_rect()
        self.next_image_rect.left = self.screen_rect.left + 20
        self.next_image_rect.bottom = self.screen_rect.bottom - 20

        self.screen.blit(self.next_image, self.next_image_rect)

    def _show_answer(self):
        font = pygame.font.SysFont(None, 36)
        # Label box
        self.show_answer_image = font.render('Show answer', True, (0, 0, 0), (110, 210, 230))
        self.show_answer_rect = self.show_answer_image.get_rect()
        self.show_answer_rect.right = self.screen_rect.right - 20
        self.show_answer_rect.bottom = self.screen_rect.bottom - 20

        self.screen.blit(self.show_answer_image, self.show_answer_rect)

    def run_quiz(self):
        while True:
            self._check_events()
            self._update_screen()


if __name__ == "__main__":
    # Make game instance and run the game.
    q = Quiz()
    q.run_quiz()
