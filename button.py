import pygame.font


class Button:
    """Creates a button on the screen."""

    def __init__(self, quiz, msg, beneath=None, right=None, left=None):
        """Initialize the button attributes."""
        self.screen = quiz.screen
        self.screen_rect = self.screen.get_rect()

        # Set the properties of the button
        self.button_color = (0, 255, 0)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, quiz.settings.button_font_size[msg])

        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()

        # Locate the button
        self.rect = self.msg_image_rect
        self.rect.center = self.screen_rect.center
        if beneath:
            self.rect.top = beneath.bottom
            self.rect.centerx = beneath.centerx
        if right:
            self.rect.left = right.right
            self.rect.centery = right.centery
        if left:
            self.rect.right = left.left
            self.rect.centery = right.centery



    def draw_button(self):
        """Draw button with message"""
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)
