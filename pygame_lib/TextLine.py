import pygame
from .Fader import Fader


class TextLine:
    def __init__(self, window, text,
                 color, font_path, font_size,
                 fps, shadow_offset=0, shadow_color=(0,0,0), startAlpha=255):

        self.window = window

        self.text = text
        self.text_surface = None

        self.color = color
        self.font = pygame.font.Font(font_path, round(font_size))

        self.shadow_surface = None
        self.shadow_offset = shadow_offset
        self.shadow_color = shadow_color

        self.fader = Fader(fps,startAlpha)
        self._render()


    def _render(self):

        if self.shadow_offset > 0:
            self.shadow_surface = self.font.render(self.text, True, self.shadow_color)
            self.shadow_rect = self.shadow_surface.get_rect()

        self.text_surface = self.font.render(self.text, True, self.color)
        self.rect = self.text_surface.get_rect()



    def fade_reset(self):
        self.fader.reset()


    def fade_in(self, duration=0.5):
        self.fader.fade_in(duration)


    def fade_out(self, duration=0.5):
        self.fader.fade_out(duration)


    def draw(self, x, y, x_offset=0, y_offset=0):

        alpha = self.fader.get_next_alpha()

        if (x == -1):
            x = self.window.get_width() // 2 - self.text_surface.get_width() // 2 + x_offset
        if (y == -1):
            y = self.window.get_height() // 2 - self.text_surface.get_height() // 2 + y_offset

        if self.shadow_offset > 0:
            self.shadow_surface.set_alpha(alpha)
            self.window.blit(self.shadow_surface, (x + self.shadow_offset, y + self.shadow_offset))

        self.text_surface.set_alpha(alpha)
        self.window.blit(self.text_surface, (x,y))



    @property
    def fade_in_started(self):
        return self.fader.fade_in_started

    @property
    def fade_out_started(self):
        return self.fader.fade_out_started

    @property
    def fade_in_ended(self):
        return self.fader.fade_in_ended

    @property
    def fade_out_ended(self):
        return self.fader.fade_out_ended
