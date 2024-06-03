import pygame, random
from enum import Enum
from pygame_lib import Utils, ScreenFader, TextLine, Timer, Color
from background import Background
from game_board import GameBoard

class GameState(Enum):
    INIT = 1
    COMPUTER_TURN = 2
    PLAYER_TURN = 3
    PLAY_ERROR = 4
    PLAY_WIN = 5
    GAME_WIN = 6
    GAME_CLEANUP = 7
    GAME_EXIT = 8
    RETURN_TO_MENU = 9
    SECRET_CHAMBER = 10

class GamePlay:
    def __init__(self, settings):
        self.settings = settings
        self.screen = pygame.display.get_surface()
        self.game_board = GameBoard(settings)
        self.background = Background(settings)
        self.screen_fader = ScreenFader(settings.fps)
        self.game_state_timer = Timer()
        self.delay_timer = Timer()
        self.score = 0
        self.score_show = False
        self.board_size = self.screen.get_height() * 440 // 480

        # links to other game screens
        # these will be assigned in game_loop.py
        self.main_menu = None
        self.secret_chamber = None

        # game state
        self.set_game_state(GameState.INIT)

    def update(self, events):

        if self.background.update(events):
            self.set_game_state(GameState.GAME_EXIT)

        player_events = []
        for event in events:
            if event.type == pygame.KEYDOWN:
                match event.key:
                    case pygame.K_ESCAPE: self.set_game_state(GameState.RETURN_TO_MENU)
                    case pygame.K_q:      self.set_game_state(GameState.GAME_EXIT)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.background.exit_button.is_clicked(event.pos):
                    self.set_game_state(GameState.RETURN_TO_MENU)

            if GameState.PLAYER_TURN:
                # if arrow key is pressed
                if event.type == pygame.KEYDOWN and \
                    event.key in [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_SPACE]:
                    player_events.append(event)

                # if mouse is moved or button is clicked
                if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEMOTION:
                    player_events.append(event)


        match self.game_state:
            case GameState.INIT:            self.init()
            case GameState.COMPUTER_TURN:   self.computer_turn()
            case GameState.PLAYER_TURN:     self.player_turn(player_events)
            case GameState.GAME_WIN:        self.game_win()
            case GameState.GAME_EXIT:       self.fade_screen()
            case GameState.RETURN_TO_MENU:  self.fade_screen()

        # fade out before going to the next screen
        if self.screen_fader.fade_out_completed:

            # if the game is over, return None to exit the game
            if self.game_state == GameState.GAME_EXIT:
                return None

            # if the game is over, return the main menu screen
            # this runs in a different class so returning link for next function to game_loop.py
            if self.game_state == GameState.RETURN_TO_MENU:
                self.cleanup()
                return self.main_menu

            if self.game_state == GameState.SECRET_CHAMBER:
                self.cleanup()
                return self.secret_chamber

        # return itself and have the game loop keep redrawing the game play screen
        return self

    def game_win(self):
        if not self.game_board.zoom_out_started:
            self.game_board.turn_off_all_tiles()
            #self.game_board.fade_out(1)
            self.show_status("You unlocked the treasure!")
            self.hide_score()
            self.zoom_out_game_board(self.settings.gameboard_zoomout_duration)
            # play rumbling sound
            self.settings.play_sound(self.settings.rumbling_sound)

        if self.game_board.zoom_out_ended:
            self.hide_status()
            self.fade_screen()

        if self.screen_fader.fade_out_completed:
            # self.cleanup()
            self.set_game_state(GameState.SECRET_CHAMBER)

    def cleanup(self):
        self.game_board.reset()
        self.screen_fader.reset()
        self.game_board.zoom_reset()
        self.set_game_state(GameState.INIT)
        self.score = 0

    def set_game_state(self, state):

        self.game_state = state
        self.status_message = ""
        self.hide_status()

        if state == GameState.COMPUTER_TURN:
            self.computer_sequence = []
            self.computer_sequence_index = 0
            self.computer_sequence_started = False
            self.computer_sequence_ended = False
            self.game_board.reset()

        if state == GameState.PLAYER_TURN:
            self.selector_tileNumber = 5
            self.player_sequence = []
            self.player_sequence_index = 0
            self.player_sequence_started = False
            self.player_sequence_ended = False

        self.game_state_timer.restart()

    def fade_screen(self):
        if not self.screen_fader.fade_out_started:
            self.screen_fader.fade_out(1)

    def fade_game_board(self):
        if not self.game_board.fade_out_started:
            self.game_board.fade_out(1)

    def zoom_out_game_board(self, duration=2):
        if not self.game_board.zoom_out_started:
            self.game_board.zoom_out(duration)

    def zoom_in_game_board(self, duration=2):
        if not self.game_board.zoom_in_started:
            self.game_board.zoom_in(duration)

    def init(self):
        if not self.game_board.fade_in_started:
            self.game_board.fade_in(1)

        if self.game_board.fade_in_ended:
            self.set_game_state(GameState.COMPUTER_TURN)

    def player_turn(self, player_events):
        # wait for player to click on the tiles in the sequence
        # that the computer pulsed
        # if player_sequence is empty, wait for player to click on a tile

        if not self.player_sequence_started:
            self.show_status("Your Turn")
            self.game_board.turn_on_selector (self.selector_tileNumber)
            self.player_sequence_started = True
            return

        if self.player_sequence_ended:
            self.hide_status()
            if self.delay_timer.get_elapsed_time() > 2500:
                if self.score == self.settings.wins_to_open_chamber:
                    self.set_game_state(GameState.GAME_WIN)
                    return

                self.set_game_state(GameState.COMPUTER_TURN)
                return

        tileNumber = 0
        tile_selected = False
        # turn on the selector tile
        if (player_events != []):
            for events in player_events:

                if events.type == pygame.MOUSEBUTTONDOWN:
                    mouse_coords = pygame.mouse.get_pos()
                    if self.game_board.coords_inside_board(mouse_coords[0], mouse_coords[1]):
                        tileNumber = self.game_board.get_tile_number_from_coords(mouse_coords[0], mouse_coords[1])
                        tile_selected = True

                elif events.type == pygame.KEYDOWN:
                    if events.key == pygame.K_UP:
                        tileNumber = self.selector_tileNumber - self.settings.num_tiles_x
                    if events.key == pygame.K_DOWN:
                        tileNumber = self.selector_tileNumber + self.settings.num_tiles_x
                    if events.key == pygame.K_LEFT:
                        tileNumber = self.selector_tileNumber - 1
                    if events.key == pygame.K_RIGHT:
                        tileNumber = self.selector_tileNumber + 1
                    if events.key == pygame.K_SPACE:
                        tileNumber = self.selector_tileNumber
                        tile_selected = True

                elif events.type == pygame.MOUSEMOTION:
                    mouse_coords = pygame.mouse.get_pos()
                    tileNumber = self.game_board.get_tile_number_from_coords(mouse_coords[0], mouse_coords[1])

        if tile_selected:
            self.game_board.turn_on_tile(tileNumber)
            self.player_sequence.append(tileNumber)
            self.player_sequence_index += 1

        elif tileNumber > 0 \
            and tileNumber <= self.settings.num_tiles_x * self.settings.num_tiles_y \
            and tileNumber != self.selector_tileNumber:

            self.game_board.turn_off_selector(self.selector_tileNumber)
            self.selector_tileNumber = tileNumber
            self.game_board.turn_on_selector(self.selector_tileNumber)

        if self.player_sequence_index < len(self.computer_sequence):
            tileNumber = None
            if tileNumber:
                self.player_sequence.append(tileNumber)
                self.player_sequence_index += 1

        # if all tiles have been clicked
        if self.player_sequence_index == len(self.computer_sequence):
            # if end-of-sequence marker not set
            if not self.player_sequence_ended:
                # code runs once when sequence is completed
                # set marker
                self.player_sequence_ended = True
                # turn off the selector tile
                self.game_board.turn_off_selector(self.selector_tileNumber)
                # restart timer
                self.delay_timer.restart()
                if self.player_sequence == self.computer_sequence:
                    self.score += 1

            if self.player_sequence == self.computer_sequence:
                self.show_status("Correct!")
            else:
                self.show_status("Incorrect!")


    def computer_turn(self):
        # generate a random sequence of numbers to pulse
        # for the player to repeat
        # if number_sequence is empty, generate a new sequence

        if not self.computer_sequence_started:
            tiles_per_sequence = self.settings.tiles_per_game_level[self.settings.difficulty]
            self.computer_sequence = random.sample(range(1,10),tiles_per_sequence)
            self.computer_sequence_index = 1
            self.computer_sequence_started = True

        self.show_status("Computer's Turn")
        self.show_score()

        tileNumber = self.computer_sequence[self.computer_sequence_index-1]

        # pulse the tiles in the sequence, wait 1.5 seconds before generating a new sequence
        if self.game_state_timer.get_elapsed_time() > 1500:

            if not self.game_board.pulse_started(tileNumber):
                self.game_board.pulse_tile(tileNumber)

            if self.game_board.pulse_ended(tileNumber):
                self.computer_sequence_index += 1

            if self.computer_sequence_index > len(self.computer_sequence):
                self.computer_sequence_ended = True
                self.hide_status()
                self.set_game_state(GameState.PLAYER_TURN)
                return

    def show_score(self):
        self.score_show = True

    def hide_score(self):
        self.score_show = False

    def show_status(self, message):
        self.status_show = True
        self.status_message = message

    def hide_status(self):
        self.status_show = False

    def hide_status(self):
        self.status_show = False

    def draw(self):
        self.background.draw()
        self.game_board.draw()

        statusTextSize = 25 * self.settings.screen_scale_x

        if self.status_show:
            statusText = TextLine(self.screen,self.status_message, Color.WHITE, self.settings.get_fontPath(self.settings.instructions_font), statusTextSize , self.settings.fps, 2)
            if not self.score_show:
                statusText.draw(-1, self.screen.get_height() - statusTextSize)
            else:
                statusText.draw(self.screen.get_width() // 2 - self.board_size // 2,
                                self.screen.get_height() - statusTextSize)

        if self.score_show:
            # show score to the right of the game board
            scoreText = TextLine(self.screen,"Score: " + str(self.score) + "/" + str(self.settings.wins_to_open_chamber), Color.WHITE, self.settings.get_fontPath(self.settings.instructions_font), statusTextSize, self.settings.fps, 2)
            scoreText.draw(self.screen.get_width() // 2 + self.board_size // 2 - (100 * self.settings.screen_scale_x),
                        self.screen.get_height() - statusTextSize)

        self.screen_fader.draw()
