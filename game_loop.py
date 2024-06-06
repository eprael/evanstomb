"""
Game Loop
---------
This is the main game loop.  It creates the game screens and links them
together.  The screens are:

- splash screen
- main menu
- game play
- secret chamber

Each one is a separate class with its own update and draw method.
The update method returns the next screen to display which can be the existing
screen or another one. The game loop then switches to the new screen.

This process continues until the game is done. The game is done when the user
quits the game or the game is over.

"""
# system libraries
import os
import pygame

# game screens
from splash_page import SplashPage
from main_menu import MainMenu
from game_play import GamePlay
from secret_chamber import SecretChamber

# settings shared by all game screens
from settings import Settings


class GameLoop:

    def __init__(self):
        """
        Initializes a new instance of the Game class.
        """
        # initialize pygame
        pygame.init()


        # load settings
        self.settings = Settings()

        # initialize sound mixer and load background music
        pygame.mixer.init()
        self.load_background_music()

        # set screen size and mode
        if self.settings.screen_mode == "fullscreen":
            # get screen size
            info_object = pygame.display.Info()
            self.settings.screen_size = (info_object.current_w,info_object.current_h)
            #
            self.screen = pygame.display.set_mode(self.settings.screen_size, pygame.FULLSCREEN)
        else:
            # use size defined in settings
            self.screen = pygame.display.set_mode(self.settings.screen_size, 0, 32)

        # graphics are sized for 800x480 screen
        # set scale for icons, torches, fonts, etc
        self.settings.screen_scale_x = self.screen.get_width() / 800.0
        self.settings.screen_scale_y = self.screen.get_height() / 480.0

        # set window title
        pygame.display.set_caption(self.settings.game_title)

        # create game screens and pass settings into each screen
        # any updates to settings (like score) will be available to all screens
        self.splash_screen = SplashPage(self.settings)
        self.main_menu = MainMenu(self.settings)
        self.game_play = GamePlay(self.settings)
        self.secret_chamber = SecretChamber(self.settings)

        # link game screens to each other
        # each game screen needs to know about the other game screens
        # splash_screen -> main_menu -> game_play -> secret_chamber -> main_menu
        self.splash_screen.main_menu = self.main_menu
        self.main_menu.game_play = self.game_play
        self.game_play.main_menu = self.main_menu
        self.game_play.secret_chamber = self.secret_chamber
        self.secret_chamber.main_menu = self.main_menu

        # set the first screen to splash screen,
        # can also set the first screen to any other screen
        # which can save time when testing

        self.current_screen = self.splash_screen
        # self.current_screen = self.main_menu
        # self.current_screen = self.game_play
        #self.current_screen = self.secret_chamber


    def load_background_music(self):
        if self.settings.background_music_sound != "" and \
           os.path.exists(self.settings.get_soundPath(self.settings.background_music_sound)):
            pygame.mixer.music.load(self.settings.get_soundPath(self.settings.background_music_sound))
            pygame.mixer.music.set_volume(self.settings.initial_music_volume)
            self.settings.background_music_available = True
        else:
            self.settings.background_music_available = False


    def run(self):
        """
        Runs the game loop, handling events and updating the screen.
        """
        clock = pygame.time.Clock()

        # start background music - only play it once
        # use volume defined in settings
        self.settings.background_music("play", self.settings.initial_music_volume)

        done = False
        while not done:
            clock.tick(self.settings.fps)
            events = pygame.event.get()

            # check for quit events
            for event in events:
                if event.type == pygame.QUIT:
                    done = True
                    break

            #if done: continue

            # call update on current screen (any of splash, main menu, game play, secret chamber)
            # update returns next screen, which can be the same or new screen
            next_screen = self.current_screen.update(events)

            # if next_screen is 'None' it means quit
            if next_screen is None:
                done = True
                continue

            # if new screen, skip updating current screen
            if next_screen != self.current_screen:
                self.current_screen = next_screen
                continue

            # redraw screen. Start with fill to black and redraw everything
            self.screen.fill((0, 0, 0))
            self.current_screen.draw()
            pygame.display.update()

        # stop and fade background music
        self.settings.background_music(False)
        pygame.quit()
