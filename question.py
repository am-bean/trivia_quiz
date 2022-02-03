import pygame
from wrapText import drawText


class Question:

    def __init__(self, quiz, prompt, answer, category):
        self.quiz = quiz
        self.prompt = prompt
        self.answer = answer
        self.category = category

    def display_question(self):
        self.display_rect = pygame.Rect(0, 0, 550, 300)
        self.display_rect.center = self.quiz.screen_rect.center
        font = pygame.font.SysFont(None, 36)
        drawText(self.quiz.screen, self.prompt, (0, 0, 0), self.display_rect, font, bkg=self.quiz.settings.bg_color)

    def check_answer(self, response):
        return response.lower().strip() == self.answer.lower().strip()

    def display_answer(self):
        self.answer_rect = pygame.Rect(0, 0, 550, 300)
        self.answer_rect.centerx = self.quiz.screen_rect.centerx
        self.answer_rect.top = self.display_rect.bottom - 50
        font = pygame.font.SysFont(None, 36)
        drawText(self.quiz.screen, self.answer, (0, 0, 0), self.answer_rect, font, bkg=self.quiz.settings.bg_color)
