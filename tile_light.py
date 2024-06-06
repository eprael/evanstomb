"""
tile_light.py
-------------
This module contains the TileLight class which is used to create the effect of a tile
being lit up.  The tile lights can be turned on and off or pulsed. It has two display modes,
one where the whole tile is lit up and the other where only the border of the tile is lit up.
Lighting the whole tile indicates that the tile is selected.  The border only display mode
displays it as a cursor and is used when the player moves around the board to select a tile.
"""

import pygame
from pygame_lib import Fader


# tile lights can have 3 configurations
# 1. on/off  - whole tile is on or off
# 2. pulsing - tile is pulsing on and off
# 3. border  - only the border of the tile is on (used for selecting a tile)
class TileLight:
    def __init__(self, screen, x, y, width, height, fps):
        self.screen=screen
        self.width = width
        self.height = height
        self.x = x
        self.y = y

        self.pulse_started = False
        self.pulse_ended = False
        self.is_pulsing = False
        self.tile_pulse_duration = 0
        self.isOn = False
        self.selectorOn = False

        self.tile_surface = pygame.Surface((self.width, self.height))
        self.tile_surface.fill((255,255,255))

        self.selector_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA )
        self.draw_tile_selector()

        self.fader = Fader(fps)
        self.surface_to_use = self.tile_surface
        self.fader.alpha = 0



    def draw_tile_selector(self):

        border_width = 8 * self.screen.get_width() // 800

        # Draw the frame as a rectangle with a transparent middle
        frame_color = (255, 255, 255, 255)  # White color with 0 transparency
        frame_rect = self.selector_surface.get_rect()
        # shrink by 10
        frame_rect.inflate_ip(-5 * 2, -5 * 2)
        frame_rect.center = self.tile_surface.get_rect().center
        pygame.draw.rect(self.selector_surface, frame_color, frame_rect)

        inner_rect = frame_rect.inflate(-border_width * 2, -border_width * 2)
        pygame.draw.rect(self.selector_surface, (0, 0, 0, 0), inner_rect)

        # draw a transparent horizontal bar in the middle
        cross_rect = frame_rect.copy()
        cross_rect.center = self.tile_surface.get_rect().center
        cross_rect.height = frame_rect.height // 2
        cross_rect.y = (frame_rect.height - cross_rect.height) // 2 + border_width

        pygame.draw.rect(self.selector_surface, (0, 0, 0, 0), cross_rect)

        # draw a transparent vertical bar in the middle
        cross_rect = frame_rect.copy()
        cross_rect.center = self.tile_surface.get_rect().center
        cross_rect.width = frame_rect.width // 2
        cross_rect.x = (frame_rect.width - cross_rect.width) // 2 + border_width
        pygame.draw.rect(self.selector_surface, (0, 0, 0, 0), cross_rect)

    def selector_on (self):
        self.selectorOn = True
        self.fader.set_alpha(200)
        self.surface_to_use = self.selector_surface

    def selector_off (self):
        self.selectorOn = False
        self.fader.set_alpha(0)
        self.surface_to_use = self.tile_surface

    def turn_on(self):
        self.isOn = True
        self.isPulsing = self.selectorOn = False
        self.fader.set_alpha(200)
        self.surface_to_use = self.tile_surface

    def turn_off(self):
        self.isOn = False
        self.fader.set_alpha(0)
        self.surface_to_use = self.tile_surface

    def pulse(self, duration=0.4):
        if not self.pulse_started:
            self.tile_pulse_duration = duration
            self.pulse_started = True
            self.pulse_ended = False
            self.is_pulsing = True
            self.surface_to_use = self.tile_surface
            self.fader.fade_in(self.tile_pulse_duration,0,170)


    def draw (self):

        self.surface_to_use = self.tile_surface

        if (self.pulse_started and not self.pulse_ended):
            alpha = self.fader.get_next_alpha()

        elif (self.isOn):
            alpha = 200
            self.surface_to_use = self.tile_surface
        elif (self.selectorOn):
            alpha = 255
            self.surface_to_use = self.selector_surface
        else:
            alpha = 0



        self.surface_to_use.set_alpha(alpha)

        self.screen.blit(self.surface_to_use, (self.x, self.y))

        if self.is_pulsing:
            if self.fader.fade_in_ended and not self.fader.fade_out_started:
                self.fader.fade_out(self.tile_pulse_duration,170,0)

            if self.fader.fade_out_ended:
                self.pulse_ended = True
                self.is_pulsing = False
