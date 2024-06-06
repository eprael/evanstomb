"""
Background class
----------------
The background class is responsible for drawing the background of the game.
It is shared by the game play and main menu screens.
It contains the background wallpaper, pharaoh, torches, and the exit button.
The background is drawn on the screen using the draw method.
The update method is used to check for events and update the game state.
The change_wallpaper method is used to change the background image randomly.
The create_exit_button method is used to create the exit button.
The draw method is used to draw the background on the screen.

"""
import pygame
from pygame_lib import Button, Utils, Sprite, Color
from pharaoh import Pharaoh


class Background:

    def __init__(self, settings):
        self.settings = settings
        self.screen = pygame.display.get_surface()

        # graphics are sized for 800 width screen
        # self.settings.screen_scale = self.screen.get_width() // 800

        self.game_exit = False
        self.default_font = settings.default_font
        self.screen_mode = settings.screen_mode
        self.fps = settings.fps

        self.exit_button = self.create_exit_button()

        # pharao sized for width of 120 on a 800x480 screen
        pharao_size = self.screen.get_width() * 120 // 800
        pharao_path = self.settings.get_imagePath("gameplay/pharao1.png")
        self.pharaoh1 = Pharaoh(self.screen, pharao_path, 5, pharao_size,
                                False,
                                self.settings.pharao_speed)

        self.pharaoh2 = Pharaoh(self.screen, pharao_path,
                                self.screen.get_width() - pharao_size - 5,
                                pharao_size,
                                True,
                                self.settings.pharao_speed)

        # torch sized for width of 470 on a 800x480 screen
        torch_path = self.settings.get_imagePath("gameplay/torch_sprite.png")
        self.torch_x = 60 * self.settings.screen_scale_x
        self.torch_y = 10 * self.settings.screen_scale_y
        self.flame1 = Sprite(self.screen, torch_path, (59.2,124), 3, self.settings.screen_scale_y)
        self.flame2 = Sprite(self.screen, torch_path, (59.2,124), 3, self.settings.screen_scale_y)

        self.game_background = None

        # save random background in settings so other screens can use it
        if self.settings.game_background is None:
            self.change_wallpaper()


    def change_wallpaper(self):
        self.settings.game_background = Utils.get_random_file_from_path(self.settings.get_imagePath("background"),True)

    def update(self, events):
        # change game_background if changed in settings
        if self.game_background != self.settings.game_background:
            self.wall_art = Utils.load_image_to_fixed_width(self.settings.game_background, self.screen.get_width(), True)
            self.game_background = self.settings.game_background


        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.exit_button.is_clicked(event.pos):
                    self.game_exit = True

        return self.game_exit

    def create_exit_button(self):
        return Button(self.screen, "X",
                       self.screen.get_width()-(15 * self.settings.screen_scale_x),
                       15*self.settings.screen_scale_y,
                       22*self.settings.screen_scale_x,
                       22*self.settings.screen_scale_y,
                       Color.RED, Color.LIGHT_RED, Color.WHITE,
                       self.settings.get_fontPath(self.default_font),
                       30 * self.settings.screen_scale_y,
                       self.settings.get_soundPath(self.settings.menu_hover_sound),
                       self.fps,
                       Color.RED, 0, 0)


    def draw(self):
        self.screen.blit(self.wall_art, (0,0))
        self.pharaoh1.draw()
        self.pharaoh2.draw()

        self.flame1.animate(self.torch_x,self.torch_y,6)
        self.flame2.animate(self.screen.get_width() - self.flame2.frame_width - self.torch_x,self.torch_y,6)

        if self.screen_mode == "fullscreen":
            self.exit_button.draw()
