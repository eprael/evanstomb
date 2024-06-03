# The settings class is used to store global game variables and settings
# that are used by the game screens. The settings class is passed to all the
# game screens from the main program (Game_loop.py)
# There are also functions at the bottom that return the full path to images, fonts, and sounds

import os
from pygame import mixer

class Settings:

    # game settings - change as needed
    #-----------------------------------------

    screen_mode = "fullscreen"  # "fullscreen" or "window"
    screen_size = (800, 480)    # "screen_size" - only applies if screen_mode is window

    num_tiles_x = 3
    num_tiles_y = 3
    fps = 60


    # folders
    #-----------------------------------------
    # main app folder
    app_dir = os.path.split(os.path.abspath(__file__))[0]

    # subfolders for images, fonts, and sounds
    image_dir = os.path.join(app_dir, "images")
    font_dir = os.path.join(app_dir, "fonts")
    sound_dir = os.path.join(app_dir, "sounds")


    # game text
    #-----------------------------------------

    instructions = [ "Instructions:",
                     "1. Computer shows a sequence of symbols",
                     "2. Player clicks the symbols in the same order",
                     "3. A successful try unlocks a secret!"
                     ]

    # each skill level gets its own win text
    # easy=artifacts, medium=Eye of Horus, Hard=Hidden Tomb
    win_text = [["You found a hidden artifact!","You uncovered an old mystery","You found a long lost toy!"],
                ["You found a priceless artifact!", "You found the Eye of Ra! ","Someone's keeping an eye on you..."],
                ["You've uncovered an ancient tomb!", "You found a room of treasure. But no way out! Goodbye!", "Someone died in here!"]]


    # game text
    #-----------------------------------------
    game_title = "Evan's Tomb"

    # fonts
    #-----------------------------------------
    default_font = 'papyrus'
    instructions_font = 'calibri'
    instructions_font_size = 25

    # animations
    #-----------------------------------------
    pharao_speed = 1                    # 0=still, 5=fast
    gameboard_zoomout_duration = 5      # 1=fast, 10=slow
    tile_pulse_duration_per_level = [0.4,0.3,0.2]           # use 0.2-0.5 where 0.2=fast, 0.5=slow

    # sounds
    #-----------------------------------------
    sound_fx_on = True
    background_music_on = True
    initial_music_volume = 0.2
    background_music_sound = "background - temple of light.ogg"
    tile_pulse_sounds = ["tile_pulse_1.ogg", "tile_pulse_2.ogg"]
    menu_hover_sound = "menu_hover.ogg"
    tile_selector_sound = "tile_selector.ogg"
    rumbling_sound = "rumble3.ogg"
    temple_chant = "deep_voice_chant2.ogg"
    secret_chamber_sound = "deep_voice_chant2.ogg"


    # internal game variables - don't change
    #-----------------------------------------
    tiles_per_game_level = [4,5,6]
    wins_to_open_chamber = 1
    difficulty = 0
    score = 0
    background_music_available = False
    background_music_playing = False
    game_background = None
    supported_extensions = [".ogg", ".mp3", ".wav"]
    game_exit = False
    # table for sound files and sound objects
    loaded_sounds = {}
    # small, medium, large boards for different screen sizes
    patternboards = ["patternboard_440.png","patternboard_1000.png","patternboard_1680.png"]
    # game is designed for 800x480 screen, but will scale to other sizes
    screen_scale_x = 1.0
    screen_scale_y = 1.0




    # application wide helper functions using above settings
    #-----------------------------------------

    def get_imagePath(self,imageName):
        return os.path.join(self.image_dir, imageName)

    def get_fontPath(self, fontName):
        return os.path.join(self.font_dir, fontName+".ttf")

    def get_soundPath(self, soundFile):
        # check if file has extension OGG, MP3, or WAV
        if not any(soundFile.endswith(ext) for ext in self.supported_extensions):
            raise ValueError("Sound file must have extension " + ", ".join(self.supported_extensions))
        return os.path.join(self.sound_dir, soundFile)


    def background_music(self, status, volume=-1, loop=False):
        if not self.background_music_available or not self.background_music_on:
            return

        if volume >= 0:
            mixer.music.set_volume(volume)

        match status:
            case "play":
                if loop: mixer.music.play(-1)
                else:    mixer.music.play()
                self.background_music_playing = True
            case "stop":
                mixer.music.stop()
                self.background_music_playing = False
            case "pause":
                #mixer.music.fadeout(2000)
                mixer.music.pause()
                self.background_music_playing = False
            case "unpause":
                #mixer.music.play(fade_ms=2000)
                mixer.music.unpause()
                mixer.music.set_volume(self.initial_music_volume)
                self.background_music_playing = True


    def play_sound(self, sound_file_name):
        if not self.sound_fx_on:
            return
        # if sound_file_name not loaded before, load and add to table
        if sound_file_name not in self.loaded_sounds:
            sound = mixer.Sound(self.get_soundPath(sound_file_name))
            self.loaded_sounds[sound_file_name] = sound
        else:
            sound = self.loaded_sounds[sound_file_name]

        mixer.find_channel().play(sound)

        # if self.settings.sound_fx_on:
        #     sound = pygame.mixer.Sound(self.get_soundPath(self.sound_file))
        #
