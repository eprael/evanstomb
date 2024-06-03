# Desc: Timer class to measure elapsed time in milliseconds
import pygame

class Timer:
    def __init__(self):
        self.start_ticks = pygame.time.get_ticks()  # Store the initial ticks

    def restart(self):
        self.start_ticks = pygame.time.get_ticks()  # Reset the start time

    def get_elapsed_time(self):
        return pygame.time.get_ticks() - self.start_ticks  # Calculate elapsed time in ms
