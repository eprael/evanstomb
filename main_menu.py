"""
main_menu.py
----------------
This module contains the MainMenu class which is the first screen the user sees
after the splash screen. The main menu screen contains the game title, instructions,
difficulty buttons, and sound buttons. The user can select the difficulty level
and turn the music and sound effects on or off. The user can also exit the game
from the main menu screen.
"""
# system libraries
import pygame

# game libraries
from pygame_lib import Button, Utils, ScreenFader, TextLine, Color, RoundedRect
from background import Background

class MainMenu:
    def __init__(self, settings):

        self.settings = settings
        self.window = pygame.display.get_surface()
        self.menu_exit = False

        # load fonts
        self.default_font_path = self.settings.get_fontPath(settings.default_font)
        self.instructions_font_path = self.settings.get_fontPath(settings.instructions_font)

        # setup text lines - 2 for the heading, 2 for the sound options
        self.heading1 = TextLine(self.window, settings.game_title, Color.WHITE, self.default_font_path, 50 * self.settings.screen_scale_x, settings.fps, 2)
        self.heading2 = TextLine(self.window, "Unlock The Code!", Color.RED, self.default_font_path, 30 * self.settings.screen_scale_x, settings.fps, 2)
        self.heading3 = TextLine(self.window, "music", Color.YELLOW, self.default_font_path, 30 * self.settings.screen_scale_x , settings.fps, 2)
        self.heading4 = TextLine(self.window, "sound", Color.YELLOW, self.default_font_path, 30 * self.settings.screen_scale_x, settings.fps, 2)


        # setup text lines for the instructions
        self.instructions = []
        for i in range(0, len(settings.instructions) ):
            self.instructions.append(TextLine(self.window,
                                              settings.instructions[i],
                                              Color.WHITE,
                                              self.instructions_font_path,
                                              self.settings.instructions_font_size * self.settings.screen_scale_x,
                                              settings.fps,
                                              2))

        # setup semi transparent window for the instructions
        rect_width = 525 * self.settings.screen_scale_x
        rect_height =  (self.instructions[0].rect.height + (10 * self.settings.screen_scale_y)) * len(self.instructions) + (15 * self.settings.screen_scale_y)
        border_width = 3 * self.settings.screen_scale_x
        self.instructions_window = RoundedRect(self.window, rect_width, rect_height,
                                               Color.LIGHT_GRAY, border_width,
                                               Color.BLACK,
                                               self.settings.fps,
                                               100)


        # setup the difficulty buttons: easy, medium, hard
        button_y = Utils.y_percent(self.window,85)
        width = 140 * self.settings.screen_scale_x
        self.easy_button = self.create_menu_button("Easy",
                                                    self.window.get_width() // 3 - (20 * self.settings.screen_scale_x),
                                                    button_y,
                                                    width)
        self.medium_button = self.create_menu_button("Medium",
                                                     self.window.get_width() // 2,
                                                     button_y,
                                                     width)
        self.hard_button = self.create_menu_button("Hard",
                                                   self.window.get_width() * 2 // 3 + (20 * self.settings.screen_scale_x),
                                                   button_y,
                                                   width)

        # setup the sound buttons: music, sound
        self.create_sound_buttons()

        # link to the game_play screen
        # gets assigned in launch.py after the game_play screen is created and
        # before the game loop starts
        self.game_play = None

        # setup the background
        self.background = Background(settings)

        # setup a fader so screen can be faded in and out
        self.screen_fader = ScreenFader(settings.fps)

    def create_sound_buttons(self):
        button_y = self.window.get_height() - (18 * self.settings.screen_scale_y)
        self.music_button = self.create_check_box(self.window.get_width() // 2 - (120 * self.settings.screen_scale_x),
                                                  button_y,
                                                  self.settings.background_music_on)
        self.sound_button = self.create_check_box(self.window.get_width() // 2 + (30 * self.settings.screen_scale_x),
                                                  button_y,
                                                  self.settings.sound_fx_on)

    def reset(self):
        self.menu_exit = False
        self.screen_fader.reset()

    def create_check_box(self, x, y, is_checked):
        if self.settings.sound_fx_on:
            hover_sound = self.settings.get_soundPath(self.settings.menu_hover_sound)
        else:
            hover_sound = ""

        if is_checked: text = "X"
        else:          text = " "

        return Button(self.window,text,
                       x, y, 30 * self.settings.screen_scale_x , 30  * self.settings.screen_scale_x,
                       Color.BLACK, Color.DARK_GRAY, Color.YELLOW,
                       self.default_font_path,16 * self.settings.screen_scale_x,
                       hover_sound,
                       self.settings.fps,
                       Color.WHITE, 1, 0)

    def create_menu_button(self, text, x, y, width):
        if self.settings.sound_fx_on:
            hover_sound = self.settings.get_soundPath(self.settings.menu_hover_sound)
        else:
            hover_sound = ""

        return Button(self.window,text,
                       x, y, width, 0,
                       Color.TAN, Color.LIGHT_TAN, Color.WHITE,
                       self.default_font_path,30 * self.settings.screen_scale_x,
                       hover_sound,
                       self.settings.fps,
                       Color.WHITE, 15, 1)

    def fade_out_center(self):
        # self.score.fade_out()
        self.heading1.fade_out()
        self.heading2.fade_out()
        self.heading3.fade_out()
        self.heading4.fade_out()

        for text_line in self.instructions:
            text_line.fade_out()

        self.instructions_window.fade_out()

        self.easy_button.fade_out()
        self.medium_button.fade_out()
        self.hard_button.fade_out()
        self.music_button.fade_out()
        self.sound_button.fade_out()


    def cleanup(self):
        self.heading1.fade_reset()
        self.heading2.fade_reset()
        self.heading3.fade_reset()
        self.heading4.fade_reset()

        for text_line in self.instructions:
            text_line.fade_reset()

        self.instructions_window.fade_reset()

        self.easy_button.fade_reset()
        self.medium_button.fade_reset()
        self.hard_button.fade_reset()
        self.music_button.fade_reset()
        self.sound_button.fade_reset()
        self.screen_fader.reset()


    def update(self, events):

        self.background.update(events)

        for event in events:

            if event.type == pygame.KEYDOWN:
                # exit game
                if event.key == pygame.K_ESCAPE:
                    self.menu_exit = True
                    self.screen_fader.fade_out()
                    break

            if event.type == pygame.MOUSEBUTTONDOWN:
                # check if the buttons are clicked
                if self.easy_button.is_clicked(event.pos):
                    self.settings.difficulty = 0
                    self.fade_out_center()


                if self.medium_button.is_clicked(event.pos):
                    self.settings.difficulty = 1
                    self.fade_out_center()

                if self.hard_button.is_clicked(event.pos):
                    self.settings.difficulty = 2
                    self.fade_out_center()

                if self.background.exit_button.is_clicked(event.pos):
                    self.menu_exit = True
                    self.screen_fader.fade_out()

                if self.music_button.is_clicked(event.pos):
                    if self.settings.background_music_on:
                        self.settings.background_music("pause")
                        self.settings.background_music_on = False
                        self.create_sound_buttons()
                    else:
                        self.settings.background_music_on = True
                        self.settings.background_music("unpause")
                        self.create_sound_buttons()

                if self.sound_button.is_clicked(event.pos):
                    self.settings.sound_fx_on = not self.settings.sound_fx_on
                    self.easy_button.play_sound = not self.easy_button.play_sound
                    self.medium_button.play_sound = not self.medium_button.play_sound
                    self.hard_button.play_sound = not self.hard_button.play_sound
                    self.music_button.play_sound = not self.music_button.play_sound
                    self.sound_button.play_sound = not self.sound_button.play_sound
                    self.create_sound_buttons()

        # fade-in first thing
        if not self.screen_fader.fade_in_started:
            self.background.change_wallpaper()
            self.screen_fader.fade_in()

        if self.heading1.fade_out_ended:
            self.cleanup()
            return self.game_play

        if self.screen_fader.fade_out_completed:
            if self.menu_exit:
                return None
            self.cleanup()
            return self.game_play

        # if the user hasn't pressed the space bar, return itself
        # and have the game loop keep redrawing the main menu screen
        return self


    def draw(self):

        self.background.draw()

        # draw the text lines on the screen
        # and increment the y with each line by the height of the text line
        y = Utils.y_percent(self.window, 5)

        self.heading1.draw(-1, y)
        y += self.heading1.rect.height + 10

        self.heading2.draw(-1, y)

        # draw centered
        self.heading3.draw(Utils.x_percent(self.window,50)-(100 * self.settings.screen_scale_x),
                           self.window.get_height() - (45 * self.settings.screen_scale_y))
        self.heading4.draw(Utils.x_percent(self.window,50)+(50 * self.settings.screen_scale_x),
                           self.window.get_height() - (45 * self.settings.screen_scale_y))


        y = Utils.y_percent(self.window, 37)

        # draw rounded rectangle with semi-transparent background
        self.instructions_window.draw(self.window,
                                      Utils.x_percent(self.window,50)-(265*self.settings.screen_scale_x),
                                      y - (10 * self.settings.screen_scale_y))

        for text_line in self.instructions:
            text_line.draw(Utils.x_percent(self.window,50)-(250*self.settings.screen_scale_x), y)
            y += text_line.rect.height + (10 * self.settings.screen_scale_y)

        self.easy_button.draw()
        self.medium_button.draw()
        self.hard_button.draw()

        self.sound_button.draw()
        self.music_button.draw()

        screen = pygame.display.get_surface()
        screen.blit(self.window, (0,0))

        self.screen_fader.draw()
