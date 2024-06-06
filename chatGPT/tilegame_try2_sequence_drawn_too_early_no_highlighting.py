import pygame
import random
import os
from pathlib import Path

# Initialize Pygame
pygame.init()

# Constants
app_dir = os.path.split(os.path.abspath(__file__))[0]

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
BOARD_SIZE = 3
TILE_SIZE = 150
MARGIN = 10
HIGHLIGHT_COLOR = (255, 255, 0)
BACKGROUND_COLOR = (255, 165, 0)
#TILE_IMAGES = ["app/images/gameplay/tile.png"] * 9  # Placeholder for your tiles
TILE_FOLDER = os.path.join(app_dir, "tiles")
TILE_IMAGES = [f"{TILE_FOLDER}/tile{i+1}.png" for i in range(9)]

# Load the Egyptian artifact images from the folder
ARTIFACT_FOLDER = os.path.join(app_dir, "artifacts")
ARTIFACT_IMAGES = [os.path.join(ARTIFACT_FOLDER, img) for img in os.listdir(ARTIFACT_FOLDER) \
                   if img.lower().endswith(('.png', '.jpg', '.jpeg'))]


# Set up screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tile Memory Game")

# Fonts
font = pygame.font.Font(None, 36)

# Classes
class Tile:
    def __init__(self, x, y, image):
        self.rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
        self.image = pygame.image.load(image)
        self.highlighted = False

    def draw(self, screen):
        if self.highlighted:
            pygame.draw.rect(screen, HIGHLIGHT_COLOR, self.rect)
        screen.blit(pygame.transform.scale(self.image, (TILE_SIZE, TILE_SIZE)), self.rect.topleft)

    def highlight(self):
        self.highlighted = True
        self.draw(screen)
        pygame.display.flip()
        pygame.time.wait(500)
        self.highlighted = False
        self.draw(screen)
        pygame.display.flip()

class Board:
    def __init__(self):
        self.tiles = []
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                x = MARGIN + (TILE_SIZE + MARGIN) * j
                y = MARGIN + (TILE_SIZE + MARGIN) * i
                image = TILE_IMAGES[i * BOARD_SIZE + j]
                self.tiles.append(Tile(x, y, image))

    def draw(self, screen):
        for tile in self.tiles:
            tile.draw(screen)

class GameManager:
    def __init__(self):
        self.board = Board()
        self.sequence = []
        self.user_sequence = []
        self.show_sequence = True
        self.sequence_index = 0
        self.is_user_turn = False

    def start_new_game(self):
        self.sequence = random.sample(self.board.tiles, 4)
        self.user_sequence = []
        self.show_sequence = True
        self.sequence_index = 0
        self.is_user_turn = False
        self.show_sequence_step()

    def show_sequence_step(self):
        for tile in self.sequence:
            tile.highlight()
            pygame.time.wait(500)  # Delay between highlights

        self.is_user_turn = True

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.is_user_turn:
            pos = pygame.mouse.get_pos()
            for tile in self.board.tiles:
                if tile.rect.collidepoint(pos):
                    self.user_sequence.append(tile)
                    tile.highlight()
                    if len(self.user_sequence) == len(self.sequence):
                        self.check_sequence()

    def check_sequence(self):
        if self.user_sequence == self.sequence:
            self.show_artifact()
        else:
            self.show_failure_message()

    def show_artifact(self):
        artifact_image = random.choice(ARTIFACT_IMAGES)
        artifact = pygame.image.load(artifact_image)
        artifact_rect = artifact.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.fill(BACKGROUND_COLOR)
        screen.blit(artifact, artifact_rect)
        pygame.display.flip()
        pygame.time.wait(2000)
        self.start_new_game()

    def show_failure_message(self):
        message = font.render("Wrong Sequence! Try Again.", True, (255, 0, 0))
        screen.fill(BACKGROUND_COLOR)
        screen.blit(message, message.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)))
        pygame.display.flip()
        pygame.time.wait(2000)
        self.start_new_game()

# Main game loop
def main():
    clock = pygame.time.Clock()
    game_manager = GameManager()
    game_manager.start_new_game()

    running = True
    while running:
        screen.fill(BACKGROUND_COLOR)
        game_manager.board.draw(screen)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            game_manager.handle_event(event)

        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
