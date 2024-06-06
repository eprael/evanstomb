"""
This is a general purpose fader class to keep track of an alpha value while
progressing through the game loop. It can be used to fade in and out images,
surfaces, text, etc.
"""

class Fader:
    def __init__(self, fps, startAlpha=255):
        # check that alpha value is between 0 and 255
        self.initial_alpha = max(0, min(255, int(startAlpha)))
        self.fps = fps
        self.reset(self.initial_alpha)


    def reset(self, startAlpha=-1):

        if startAlpha == -1: self.alpha = self.initial_alpha
        else:                self.alpha = startAlpha

        self.target_alpha = 0
        self.alpha_step = 0
        self.fade_in_started = False
        self.fade_in_ended = False
        self.fade_out_started = False
        self.fade_out_ended = False

    # fades in the alpha value of the fader
    # duration is the time in seconds to fade out
    # fps is the frames per second of the game
    # startAlpha is the alpha value to start the fade out from
    # if startAlpha is -1, the current alpha value is used
    # targetAlpha is the alpha value to fade out to
    def fade_in(self, duration, startAlpha=0, targetAlpha=255):

        if not self.fade_in_started:
            self.fade_in_started = True
            if startAlpha != -1:
                self.alpha = startAlpha
            self.target_alpha = targetAlpha
            self.alpha_step = (abs(self.target_alpha - self.alpha)) / (duration * self.fps)
            #self.alpha_step = 1 / (duration * self.fps)

    # fades out the alpha value of the fader
    # duration is the time in seconds to fade out
    # fps is the frames per second of the game
    # startAlpha is the alpha value to start the fade out from
    # if startAlpha is -1, the current alpha value is used
    # targetAlpha is the alpha value to fade out to
    def fade_out(self, duration, startAlpha=-1, targetAlpha=0):

        if not self.fade_out_started:
            self.fade_out_started = True
            if startAlpha != -1:
                self.alpha = startAlpha
            self.target_alpha = targetAlpha
            self.alpha_step = -(abs(self.target_alpha - self.alpha)) / (duration * self.fps)


    def is_fading(self):
        return ((self.fade_in_started and not self.fade_in_ended) or
                (self.fade_out_started and not self.fade_out_ended))

    def get_next_alpha(self):

        if self.is_fading():
            self.alpha += self.alpha_step
            self.alpha = max(0, min(255, int(self.alpha)))

            if self.fade_in_started and self.alpha >= self.target_alpha:
                self.fade_in_ended = True
            if self.fade_out_started and self.alpha <= self.target_alpha:
                self.fade_out_ended = True

        return self.alpha


    def set_alpha(self, alpha):
        self.alpha = alpha
        self.alpha_step = 0