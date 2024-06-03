import math
import random
import pygame
from pygame_lib import Utils, Timer

class Pharaoh:
    def __init__(self, screen, imagePath, x, width, face_left=False, pharao_speed = 0.5):
        self.screen=screen
        self.pharaoh = Utils.load_image_to_fixed_width(imagePath, width, True)
        self.width = width
        self.x = x
        self.y = self.screen.get_height() - self.pharaoh.get_height() - 1
        self.is_first_delay = True

        self.x_delta = pharao_speed

        range_of_motion = self.pharaoh.get_width() // 3

        if face_left:
            self.x_range = (x-range_of_motion, x+self.pharaoh.get_width()+30)
            self.flip()
            # correction for flip
            self.x = self.screen.get_width() - self.pharaoh.get_width() - 5
        else:
            self.x_range = (x-self.pharaoh.get_width()-30, x+range_of_motion)


        self.delay_timer = Timer()
        self.delay_range = (5, 10)

        self.init_defaults()

    def flip(self):
        self.pharaoh = pygame.transform.flip(self.pharaoh, True, False)
        self.x_delta = -self.x_delta
        if self.x_delta < 0:
            self.x = self.x - (self.pharaoh.get_width() * 60//252 )
        else:
            self.x = self.x + (self.pharaoh.get_width() * 60//252 )

    def init_defaults(self):
        self.delay_in_progress = False
        self.delay_length = 0
        self.count_down = 0
        self.delay_timer.restart()


    def draw (self):
        self.screen.blit(self.pharaoh, (self.x, self.y))

        if abs(self.x_delta) > 0:
            if not self.delay_in_progress :
                # On 0 a new delay is initiated
                if self.count_down <= 0:
                    # initiate random delay
                    self.delay_in_progress = True
                    self.delay_length = math.floor(random.randint(self.delay_range[0], self.delay_range[1]) * 1000)
                    self.delay_timer.restart()
                else:
                    self.count_down -= 1
                    self.x = self.x + self.x_delta

                    if  self.x < self.x_range[0] or self.x > self.x_range[1]:
                        self.flip()
                        self.count_down = 0
            else:
                if self.delay_timer.get_elapsed_time() > self.delay_length:
                    self.delay_in_progress = False
                    self.count_down = random.randint(200, 400)
                    if random.randint(1, 100) <= 10:
                        self.flip()
                        self.count_down = 0
