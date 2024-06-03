import pygame

class ScreenFader:
    # fades the whole screen by adding a surface overtop the
    # existing screen and changing the alpha value of the surface.
    # The surface can be any color, so you can fade to black, white, etc.
    def __init__(self, fps):
        self.screen = pygame.display.get_surface()
        self.fps = fps
        self.fade_surface = pygame.Surface((self.screen.get_width(), self.screen.get_height() ))
        self.color = (0,0,0)    # default fade to, or fade from color
        self.fade_surface.fill(self.color)
        self.reset()

    def reset(self):
        self.alpha = 0
        self.alpha_step = 0

        self.fade_in_started = False
        self.fade_in_completed = False
        self.fade_out_started = False
        self.fade_out_completed = False

    def fade_in(self, duration=0.5, color=(0,0,0)):
        # fading in by fading out a black screen from full alpha to none
        if not self.fade_in_started and not self.fade_in_completed:
            self.fade_in_started = True
            self.alpha_step = -255 / (duration * self.fps)
            #self.alpha_step = -1 / (duration * self.fps)
            self.alpha = 255
            self.color = color

    def fade_out(self,duration=0.5, color=(0,0,0)):
        # fading out by fading in a black screen (no alpha to full)
        if not self.fade_out_started and not self.fade_out_completed:
            self.fade_out_started = True
            self.alpha_step = 255 / (duration * self.fps)
            #self.alpha_step = 1 / (duration * self.fps)
            self.alpha = 0
            self.color = color

    @property
    def fade_out_complete(self):
        return self.fade_out_completed

    @property
    def fade_in_complete(self):
        return self.fade_in_completed

    @property
    def fade_in_progress(self):
        return self.fade_in_started and not self.fade_in_completed

    @property
    def fade_out_progress(self):
        return self.fade_out_started and not self.fade_out_completed


    def draw(self):
        if self.fade_in_progress or self.fade_out_progress:
            self.fade_surface.set_alpha(self.alpha)
            self.screen.blit(self.fade_surface, (0,0))

            self.alpha += self.alpha_step
            if self.fade_out_progress and self.alpha >= 255:
                self.fade_out_completed = True
            if self.fade_in_progress and self.alpha <= 0:
                self.fade_in_completed = True
