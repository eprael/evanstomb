"""
This is a general purpose class to keep track of a zoom value while
progressing through the game loop. It can be used to zoom in and out images,
surfaces, text, etc.
"""

class Zoomer:
    def __init__(self, fps, startZoom=100):
        # check that zoom value is between 0 and 100
        self.initial_zoom = max(0, min(100, startZoom))
        self.fps = fps
        self.reset()


    def reset(self, startZoom=-1):

        if startZoom == -1: self.zoom = self.initial_zoom
        else:               self.zoom = startZoom

        self.target_zoom = 0
        self.zoom_step = 0
        self.zoom_in_started = False
        self.zoom_in_ended = False
        self.zoom_out_started = False
        self.zoom_out_ended = False

    # zooms into the zoom value of the Shrinker
    # duration is the time in seconds to zoom out
    # fps is the frames per second of the game
    # startZoom is the zoom value to start the zoom out from
    # if startZoom is -1, the current zoom value is used
    # targetZoom is the zoom value to zoom out to
    def zoom_in(self, duration, startZoom=0, targetZoom=100):

        if not self.zoom_in_started:
            self.zoom_in_started = True
            if startZoom != -1:
                self.zoom = startZoom
            self.target_zoom = targetZoom
            self.zoom_step = (abs(self.target_zoom - self.zoom)) / (duration * self.fps)
            #self.zoom_step = 1 / (duration * self.fps)

    # zooms out the zoom value of the Shrinker
    # duration is the time in seconds to zoom out
    # fps is the frames per second of the game
    # startZoom is the zoom value to start the zoom out from
    # if startZoom is -1, the current zoom value is used
    # targetZoom is the zoom value to zoom out to
    def zoom_out(self, duration, startZoom=-1, targetZoom=0):

        if not self.zoom_out_started:
            self.zoom_out_started = True
            if startZoom != -1:
                self.zoom = startZoom
            self.target_zoom = targetZoom
            self.zoom_step = -(abs(self.target_zoom - self.zoom)) / (duration * self.fps)
            temp=0



    def is_zooming(self):
        return ((self.zoom_in_started and not self.zoom_in_ended) or
                (self.zoom_out_started and not self.zoom_out_ended))

    def get_next_zoom(self):

        if self.is_zooming():
            self.zoom += self.zoom_step
            self.zoom = max(0, min(100, self.zoom))

            if self.zoom_in_started and self.zoom >= self.target_zoom:
                self.zoom_in_ended = True
            if self.zoom_out_started and self.zoom <= self.target_zoom:
                self.zoom_out_ended = True

        return self.zoom


    def set_zoom(self, zoom):
        self.zoom = zoom
        self.zoom_step = 0