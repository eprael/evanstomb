import pygame
import random
import os

from pygame_lib import Button, Utils, TextLine, ScreenFader, Color


class SecretChamber:
    def __init__(self, settings):

        self.settings = settings
        self.window = pygame.display.get_surface()
        self.game_exit = False
        self.default_font_path = self.settings.get_fontPath(settings.default_font)
        self.background_img = None
        self.heading = None
        button_y = self.window.get_height() - (40 * self.settings.screen_scale_y)
        button_x = self.window.get_width() - (80 * self.settings.screen_scale_x)
        width = 140 * self.settings.screen_scale_x

        self.menu_button = self.create_menu_button("Continue", button_x , button_y, width)

        # gets assigned in launch.py before the game loop starts
        self.game_play = None

        self.screen_fader = ScreenFader(settings.fps)  # creates a new surface to fade screen in and out
        self.reset()

    def reset(self):
        self.game_exit = False
        self.screen_fader.reset()



    def create_menu_button(self, text, x, y, width):
        if self.settings.sound_fx_on:
            hover_sound = self.settings.get_soundPath(self.settings.menu_hover_sound)
        else:
            hover_sound = ""

        return Button(self.window,text,
                       x, y, width, 0,
                       (188,113,55), (214,150,89), Color.WHITE,
                       #Color.BLUE, Color.LIGHT_BLUE, Color.WHITE,
                       self.default_font_path,30 * self.settings.screen_scale_x,
                       hover_sound,
                       self.settings.fps,
                       Color.WHITE, 15, 1)



    def update(self, events):


        for event in events:
            if event.type == pygame.KEYDOWN:
                # exit game
                if event.key == pygame.K_ESCAPE:
                    self.game_exit = True
                    self.screen_fader.fade_out()
                    break

            if event.type == pygame.MOUSEBUTTONDOWN:
                # check if the buttons are clicked
                if self.menu_button.is_clicked(event.pos):
                    self.settings.difficulty = 0
                    self.screen_fader.fade_out()



        # fade-in first thing
        if not self.screen_fader.fade_in_started:
            self.screen_fader.fade_in()
            backgroundPath = Utils.get_random_file_from_path(self.settings.get_imagePath("chamber/"+str(self.settings.difficulty)),True)
            self.background_img = Utils.load_image_to_fixed_height(backgroundPath, self.window.get_height() * 380 // 480, True)
            heading_text = self.settings.win_text[self.settings.difficulty][random.randint(0,2)]
            # match self.settings.difficulty:
            #     case 0: heading_text = "You found an Ancient Artifact!"
            #     case 1: heading_text = "You found the Eye of Horus!"
            #     case 2: heading_text = "You found a Hidden Tomb!"

            self.heading = TextLine(self.window, heading_text, Color.WHITE, self.default_font_path, 30 * self.settings.screen_scale_x , self.settings.fps, 2)
            #self.settings.background_music("pause")
            self.settings.play_sound(self.settings.secret_chamber_sound)


        if self.screen_fader.fade_out_completed:
            self.reset()
            if self.game_exit:
                return None
            #self.settings.background_music("unpause")
            return self.main_menu

        # if the user hasn't pressed the space bar, return itself
        # and have the game loop keep redrawing the main menu screen
        return self

    def draw(self):

        #self.window.blit(self.background_img, (0,0))
        # draw image centered on screen

        self.window.blit(self.background_img,
                        (self.window.get_width() // 2 - self.background_img.get_width() // 2,
                        self.window.get_height() // 2 - self.background_img.get_height() // 2 + 20))

        # draw the text lines on the screen
        # and increment the y with each line by the height of the text line
        y = Utils.y_percent(self.window, 2)

        self.heading.draw(-1, y)
        y += self.heading.rect.height -20

        # self.heading2.draw(-1, y)
        # y += self.heading2.rect.height

        #self.score = TextLine(self.window, "Score:" + str(self.settings.score), Color.WHITE, self.default_font_path, 25, self.settings.fps, 2)
        #self.score.draw(-1, y)
        #y += self.score.rect.height + 10


        self.menu_button.draw()

        # mouse_pos = pygame.mouse.get_pos()
        # Utils.write_text(self.window, 'x:'+ str(mouse_pos[0])+
        #                             ', y:'+str(mouse_pos[1]),
        #                             0, 0, 0, 0, Color.WHITE, 'calibri', 10, 1)

        screen = pygame.display.get_surface()
        screen.blit(self.window, (0,0))

        self.screen_fader.draw()
