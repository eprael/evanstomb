"""
This is a general purpose button class that can be used to create buttons with
text on them. The button can be sized to fit the text or a specific width and
height can be set. The button can be centered on the screen or placed at a
specific x,y coordinate. The button can have a hover color, text color, and
button color. The button can have a border with a specific color, width, and
radius. The button can also play a sound when hovered over.
"""
import pygame
from .Fader import Fader

class Button:
    # width and height of 0 means the button will be sized to fit the text
    # x and y of -1 means the button will be centered on the screen
    # x and y are the button's center coordinates

    def __init__(self, window, text,
                 x, y, w, h,
                 button_color, hover_color, text_color,
                 font_path, font_size, hover_sound_path,
                 fps,
                 border_color, border_radius, border_width):

        #self.window = pygame.display.get_surface()
        self.window = window

        self.text = text

        self.w = w
        self.h = h
        self.x = x
        self.y = y
        self.width=w
        self.height=h
        self.button_area = pygame.Rect(x, y, w, h)
        self.sound_on = False

        self.button_color = button_color
        self.hover_color = hover_color
        self.text_color = text_color

        self.border_color = border_color
        self.border_radius = border_radius
        self.border_width = border_width
        self.play_sound = False

        self.hover_sound = None
        if hover_sound_path != "":
            self.hover_sound = pygame.mixer.Sound(hover_sound_path)
            self.play_sound = True

        self.font = pygame.font.Font(font_path, round(font_size))

        self.was_hovered = False

        self.fader = Fader(fps)
        self.render()


    def fade_reset(self):
        self.fader.reset()

    def fade_in(self, duration=0.5):
        self.fader.fade_in(duration)

    def fade_out(self, duration=0.5):
        self.fader.fade_out(duration)

    def set_alpha(self, alpha):
        self.fader.set_alpha(alpha)

    def turn_sound_on(self):
        self.play_sound = True

    def turn_sound_off(self):
        self.play_sound = False

    def is_hovered(self):
        mouse_pos = pygame.mouse.get_pos()
        return self.button_area.collidepoint(mouse_pos)

    # draw a rounded rectangle with border
    def draw_rounded_rect(self,surface,
                          x, y, width, height,
                          color,
                          border_radius, border_width=0, border_color=(0, 0, 0)):

        # Create a rect to store the position and size of the rectangle
        rect = pygame.Rect(x, y, width, height)

        if border_width > 0:
            if border_radius > 0:
                # Draw outer rectangle with border color
                pygame.draw.rect(surface, border_color, rect, border_radius=border_radius)
                # Draw inner rectangle with fill color
                pygame.draw.rect(surface, color, rect.inflate(-border_width*2, -border_width*2), border_radius=border_radius)
            else:

                # Draw outer rectangle with border color
                pygame.draw.rect(surface, border_color, rect)
                # Draw inner rectangle with fill color
                pygame.draw.rect(surface, color, rect.inflate(-border_width*2, -border_width*2))
        else:
            pygame.draw.rect(surface, color, rect, border_radius=border_radius)



    # separting render and draw
    # render creates the button while draw displays it
    # only if there is a change in hover state will the button be re-rendered
    def render(self):

        # Rendering text surface
        self.text_surf = self.font.render(self.text, True, self.text_color)
        self.text_rect = self.text_surf.get_rect()

        # create button surface
        # width or height of 0 means auto; set to the width/height of the text + 10
        if self.w == 0: self.width = self.text_rect.width + 10
        if self.h == 0: self.height = self.text_rect.height + 10
        self.button_surf = pygame.Surface((self.width, self.height), pygame.SRCALPHA, 32)
        self.button_rect = self.button_surf.get_rect()

        # x or y of -1 = centered on window
        if self.x == -1: self.x = self.window.get_width() // 2
        if self.y == -1: self.y = self.window.get_height() // 2

        # check if hover in progress and select appropriate color
        if self.is_hovered(): color_to_use = self.hover_color
        else:                 color_to_use = self.button_color

        # if radius is greater than 0, draw a rounded rectangle
        # else draw regular rectangle with border
        if self.border_radius > 0:
            # draw rounded rectangle with border
            self.draw_rounded_rect(self.button_surf,
                                   # x,y,width,height
                                   0, 0, self.width,self.height,
                                   # color
                                   color_to_use,
                                   # border_radius, border_width, border_color
                                   self.border_radius,2,self.border_color)

        else:
            # draw regular rectangle with border
            if self.border_width > 0:
                # draw rectangle with border color
                pygame.draw.rect(self.button_surf, self.border_color, self.button_surf.get_rect())
                # draw rectangle with button color inside border
                pygame.draw.rect(self.button_surf, color_to_use, self.button_surf.get_rect().inflate(-self.border_width*2, -self.border_width*2))
            else:
                pygame.draw.rect(self.button_surf, color_to_use, self.button_surf.get_rect())

        # center text surface on button surface and blit
        self.text_rect.center = self.button_rect.center
        self.button_surf.blit(self.text_surf, self.text_rect)

        # create screen area from button area and center on x,y
        self.button_area = self.button_rect
        self.button_area.center = (self.x, self.y)



    def draw (self):

        # if change in hover re-render button
        if (self.is_hovered() != self.was_hovered):
            self.render()
            if self.is_hovered() and self.play_sound:
                pygame.mixer.find_channel().play(self.hover_sound)
            self.was_hovered = not self.was_hovered

        alpha = self.fader.get_next_alpha()
        self.button_surf.set_alpha(alpha)
        self.window.blit(self.button_surf, self.button_area.topleft)


    def is_clicked(self, coords):
        return self.button_area.collidepoint(coords)
