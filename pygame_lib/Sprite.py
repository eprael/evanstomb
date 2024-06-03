import math
import pygame
import os

from .Utils import Utils

class Sprite:
    def __init__(self, screen, image, frame_dimensions, num_frames, scale=1):
        # Load the spritesheet
        self.spritesheet = Utils.load_image(image, True )
        # scale image to scale
        if scale != 1:
            self.spritesheet = pygame.transform.scale(self.spritesheet,
                                                     (int(self.spritesheet.get_width() * scale),
                                                      int(self.spritesheet.get_height() * scale)))
            self.frame_width = frame_dimensions[0] * scale
            self.frame_height = frame_dimensions[1] * scale
        else:
            self.frame_width, self.frame_height = frame_dimensions

        self.num_frames = num_frames
        self.screen = screen
        self.frames = self.load_frames()
        self.frame_idx = -1

    def load_frames(self):
        # Extract frames from the spritesheet
        frames = []
        for i in range(self.num_frames):
            rect = pygame.Rect(math.floor(i * self.frame_width), 0, math.floor(self.frame_width), math.floor(self.frame_height))
            frame = self.spritesheet.subsurface(rect)
            frames.append(frame)
        return frames

    def animate(self, x, y, fps):
        # Update the frame index
        # time.get_ticks() returns the number of milliseconds since the program started
        # // (1000 // fps) is the number of milliseconds per frame
        # independent frame rate
        self.frame_idx = (pygame.time.get_ticks() // (1000 // fps)) % len(self.frames)
        self.frame_idx = (self.frame_idx + 1) % self.num_frames
        # Draw the current frame
        self.screen.blit(self.frames[self.frame_idx], (x, y))

# Usage example outside of the class
# def main():
#     pygame.init()
#     screen_width = 800
#     screen_height = 600
#     screen = pygame.display.set_mode((screen_width, screen_height))
#     clock = pygame.time.Clock()
#     fps = 10

#     # Create a SpriteAnimation object
#     sprite_animation = Sprite('path_to_spritesheet.png', (64, 64), 10)

#     running = True
#     while running:
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 running = False

#         screen.fill((0, 0, 0))  # Clear the screen with black
#         sprite_animation.animate(screen, 100, 100, fps, clock)  # Animate the sprite

#         pygame.display.flip()
#         clock.tick(60)  # Run the game loop at 60 FPS

#     pygame.quit()

# if __name__ == '__main__':
#     main()
