"""
SplashPage screen
This is the first screen that is displayed when the game is launched. It displays
the game title and a random image from the splash folder. The screen fades in and
out when it appears and disappears. The player can skip the screen by pressing
the a key or clicking the mouse.
"""
import pygame
from pygame.locals import *
from pygame_lib import Utils, TextLine, ScreenFader, Timer, Color


class SplashPage:
    def __init__(self, settings):
        self.settings = settings
        self.screen = pygame.display.get_surface()
        self.screen_fader = ScreenFader(settings.fps)
        self.timer = Timer()

        # load random background image and scale to screen width
        imageFile = Utils.get_random_file_from_path(settings.get_imagePath("splash"),True)
        self.splash_image = Utils.load_image_to_fixed_width(imageFile, self.screen.get_width())

        # create text image for game title
        self.title_text = TextLine(self.screen, settings.game_title,
                                   # color, font_path, font_size, shadow_offset
                                   Color.WHITE, self.settings.get_fontPath(self.settings.default_font), 90 * self.settings.screen_scale_x, settings.fps, 2, Color.BLACK,0)

        # this will be replaced with the main menu screen object created in launch.py
        # before the game loop starts
        # it's a reference to the main menu screen object and will be returned
        # when the splash screen is done to let the game loop know to switch to the main menu
        self.main_menu = None


    # update method determines and returns the next game screen
    # based on the events that have occurred
    # it will either return itself or the next game screen

    def update(self, events):

        for event in events:
            if event.type == pygame.KEYDOWN:
                # if ESC is pressed, quit the game
                if event.key == pygame.K_ESCAPE:
                    return None
                else:
                    self.settings.background_music("unpause")
                    return self.main_menu

            if event.type == pygame.MOUSEBUTTONDOWN:
                self.settings.background_music("unpause")
                return self.main_menu

        # first thing - fade-in and play temple chant
        if not self.screen_fader.fade_in_started:
            self.screen_fader.fade_in(2)
            self.settings.background_music("pause")
            self.settings.play_sound(self.settings.temple_chant)


        if self.screen_fader.fade_in_completed and not self.title_text.fade_in_started:
            self.title_text.fade_in(2)

        #if self.timer.get_elapsed_time() > 5000 and not self.title_text.fade_out_started:
        #    self.title_text.fade_out(1)

        # Wait N seconds and start screen fade out
        if self.timer.get_elapsed_time() > 9000 and not self.screen_fader.fade_out_started:
            self.screen_fader.fade_out(1)

        # after screen has faded out, switch to main menu
        # splash page will not be seen again
        if self.screen_fader.fade_out_completed:
            self.settings.background_music("unpause")
            return self.main_menu

        # pan splash image up
        # self.viewFrame_rect.y -= self.viewFrame_delta
        # if self.viewFrame_rect.y < 0:
        #     self.viewFrame_rect.y = 0


        # Otherwise, draw the splash screen again on the next game loop
        return self


    def draw(self):

        # draw background
        self.screen.blit(self.splash_image, (0,0))
        #self.screen.blit(self.splash_pan_image, (0,0), self.viewFrame_rect)

        # draw game title
        if self.timer.get_elapsed_time() > 2000:
            self.title_text.draw(-1,-1)

        # draw screen fader
        self.screen_fader.draw()
