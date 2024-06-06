"""
This is a general purpose rounded rectangle class that can be used to create
rounded rectangles with a border and an inside color. The rounded rectangle
can be faded in and out. The rounded rectangle can be drawn at a specific
x,y coordinate or centered on the screen. The rounded rectangle can have a
specific width, height, border color, border width, and inside color.
"""
import pygame
from .Fader import Fader

class RoundedRect:
    def __init__(self, window,
                 width, height,
                 border_color, border_width,
                 inside_color,
                 fps,
                 start_alpha=255):

        self.window = window
        self.width = width
        self.height = height
        self.border_color = border_color
        self.border_width = border_width
        self.inside_color = inside_color
        self.start_alpha = start_alpha

        self.fader = Fader(fps,start_alpha)


    def fade_reset(self):
        self.fader.reset()


    def fade_in(self, duration=0.5):
        self.fader.fade_in(duration)


    def fade_out(self, duration=0.5):
        self.fader.fade_out(duration)


    def draw(self, window, x, y):

        alpha = self.fader.get_next_alpha()

        # if (x == -1):
        #     x = self.window.get_width() // 2 - self.text_surface.get_width() // 2 + x_offset
        # if (y == -1):
        #     y = self.window.get_height() // 2 - self.text_surface.get_height() // 2 + y_offset



         # Create a temporary surface to draw the inside part with transparency
        temp_surface = pygame.Surface((self.width - 2 * self.border_width, self.height - 2 * self.border_width), pygame.SRCALPHA)

        # Set transparency for the inside part
        temp_surface.set_alpha(alpha)

        # Draw the inner rounded rectangle on the temporary surface
        pygame.draw.rect(temp_surface, self.inside_color,
                         (0, 0, self.width - 2 * self.border_width, self.height - 2 * self.border_width), border_radius=15)

        if self.fader.fade_out_started:
            # Draw the border rounded rectangle on the main surface
            pygame.draw.rect(temp_surface, self.border_color, (round(x), round(y), round(self.width), round(self.height)), round(self.border_width), border_radius=15)
            # Blit the temporary surface onto the main surface
            window.blit(temp_surface, (x + self.border_width, y + self.border_width))
        else:
            # Blit the temporary surface onto the main surface
            window.blit(temp_surface, (x + self.border_width, y + self.border_width))

            # Draw the border rounded rectangle on the main surface
            pygame.draw.rect(window, self.border_color, (round(x), round(y)-1, round(self.width), round(self.height)), round(self.border_width), border_radius=15)



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
