"""
Game Board
----------
This class is responsible for managing the game board. It is responsible for
drawing the game board and the tiles. It also manages the zooming and fading
effects for the game board. It also manages the tile lights and their pulsing
effects.

The game board is a fixed size image that is centered on the screen. The tiles
are drawn on top of the game board. The tiles are arranged in a grid pattern.
The tiles can be turned on and off. The tiles can also be pulsed to create a
flashing effect.

(comments generated with github copilot)
"""

import math
import pygame
from pygame_lib import Utils, Fader, Zoomer

from tile_light import TileLight


class GameBoard:

    def __init__(self, settings):
        self.settings = settings
        self.screen = pygame.display.get_surface()
        self.fader = Fader(self.settings.fps)
        self.zoomer = Zoomer(self.settings.fps)

        # load sounds
        self.last_pulse_sound = 0
        self.pulse_sounds = []
        for pulse_sound in self.settings.tile_pulse_sounds:
            self.pulse_sounds.append(pulse_sound)

        # setup game board
        board_height = self.screen.get_height() * 440 // 480
        if board_height <= 480:     board_file_name = self.settings.patternboards[0]
        elif board_height <= 1200:  board_file_name = self.settings.patternboards[1]
        else:                       board_file_name = self.settings.patternboards[2]

        self.board_image_path = self.settings.get_imagePath("gameplay/" + board_file_name)
        self.game_board_full = Utils.load_image_to_fixed_height(self.board_image_path, board_height, True)
        self.tiles = []
        self.setup_game_board()


        # calculate tile size
        self.num_tiles = self.settings.num_tiles_x * self.settings.num_tiles_y
        self.tile_width = self.board_width // self.settings.num_tiles_x
        self.tile_height = self.board_height // self.settings.num_tiles_y
        self.tile_number = 0

        self.reset()

    def reset(self):
        # must be called after setup_game_board
        self.setup_game_board(100)
        self.setup_tiles()
        self.fade_reset()
        self.zoom_reset()
        self.turn_off_all_tiles()




    def setup_game_board(self, zoom_level=100):

        self.game_board = self.game_board_full.copy()

        if zoom_level != 100:
            scale_x = self.game_board.get_width() * zoom_level // 100
            scale_y = self.game_board.get_height() * zoom_level // 100
            self.game_board = pygame.transform.scale(self.game_board, (scale_x, scale_y))

        self.board_width = self.game_board.get_width()
        self.board_height = self.game_board.get_height()

        # center board on screen
        self.game_board_rect = self.game_board.get_rect()
        self.game_board_rect.center = self.screen.get_rect().move(0,-10).center
        #self.game_board_rect.y = 10
        self.board_x, self.board_y = self.game_board_rect.topleft


    def setup_tiles(self):

        # setup tile collection
        self.tiles = []

        for i in range(1, self.num_tiles + 1):
            tile_x, tile_y = self.get_coords_from_tile_number(i)
            tile = TileLight(self.screen,
                        # x,y
                        self.board_x + tile_x, self.board_y + tile_y,
                        # width, height
                        self.tile_width, self.tile_height,
                        self.settings.fps)

            self.tiles.append(tile)


    def turn_off_all_tiles(self):
        for tile in self.tiles:
            tile.turn_off()
            tile.selector_off()


    def turn_on_tile(self, tile_number):
        self.tiles[tile_number-1].turn_on()
        self.pulse_play_sound()

    def turn_on_selector(self, tile_number):
        self.tiles[tile_number-1].selector_on()
        self.settings.play_sound(self.settings.tile_selector_sound)

    def turn_off_selector(self, tile_number):
        self.tiles[tile_number-1].selector_off()

    def pulse_ended(self, tile_number):
        return self.tiles[tile_number-1].pulse_ended

    def pulse_started(self, tile_number):
        return self.tiles[tile_number-1].pulse_started

    def is_pulsing(self, tile_number):
        return self.tiles[tile_number-1].is_pulsing

    def pulse_play_sound(self):
        if not self.settings.sound_fx_on:
            return
        # alternate between multiple pulse sounds
        self.last_pulse_sound += 1
        if self.last_pulse_sound >= len(self.pulse_sounds):
            self.last_pulse_sound = 0

        self.settings.play_sound(self.pulse_sounds[self.last_pulse_sound])

    def pulse_tile(self, tile_number):
        if not self.is_pulsing(tile_number):
            self.tile_number = tile_number
            self.tiles[tile_number-1].pulse(self.settings.tile_pulse_duration_per_level[self.settings.difficulty])
            self.pulse_play_sound()


    def get_coords_from_tile_number(self,tile_num):
        x = (tile_num-1) % self.settings.num_tiles_x
        y = math.floor((tile_num-1) / self.settings.num_tiles_y)
        return x * self.tile_width, y * self.tile_height

    def coords_inside_board(self, x, y):
        return self.game_board_rect.collidepoint(x, y)

    def get_tile_number_from_coords(self, x, y):
        # if the x,y coordinates are not on the game board, return 0
        if not self.coords_inside_board(x, y):
            return 0
        x -= self.board_x
        y -= self.board_y
        tile_x = math.floor(x / self.tile_width)
        tile_y = math.floor(y / self.tile_height)

        # another out-of-bounds check
        tile_x = min(tile_x, self.settings.num_tiles_x - 1)
        tile_y = min(tile_y, self.settings.num_tiles_y - 1)

        return tile_y * self.settings.num_tiles_x + tile_x + 1


    def zoom_reset(self):
        self.zoomer.reset()

    def zoom_in(self, duration=3):
        self.zoomer.zoom_in(duration)

    def zoom_out(self, duration=3):
        self.zoomer.zoom_out(duration)


    def fade_reset(self):
        self.fader.reset()

    def fade_in(self, duration=0.5):
        self.fader.fade_in(duration)

    def fade_out(self, duration=0.5):
        self.fader.fade_out(duration)


    def tile_is_on(self, tile_number):
        return self.tiles[tile_number-1].isOn

    def draw(self):
        zoom = self.zoomer.get_next_zoom()
        if zoom < 100:
            self.setup_game_board(zoom)

        alpha = self.fader.get_next_alpha()
        self.game_board.set_alpha(alpha)

        self.screen.blit(self.game_board, (self.board_x, self.board_y))

        for tile in self.tiles:
            tile.draw()


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


    @property
    def zoom_in_started(self):
        return self.zoomer.zoom_in_started

    @property
    def zoom_out_started(self):
        return self.zoomer.zoom_out_started

    @property
    def zoom_in_ended(self):
        return self.zoomer.zoom_in_ended

    @property
    def zoom_out_ended(self):
        return self.zoomer.zoom_out_ended
