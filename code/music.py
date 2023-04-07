from pygame import music

class Music:
    def init(self):
        self.music_playing = False      # Add this line to initialize the attribute music_playing as False


def play_music(self, music_file):
    """Function to play a music file"""
    music.load(music_file)
    music.play()
    self.music_playing = True       # Add this line to set the attribute music_playing as True

def stop_music(self):
    """Function to stop the currently playing music"""
    music.stop()
    self.music_playing = False      # Add this line to set the attribute music_playing as False

def is_music_playing(self):
    """Function to check if music is currently playing"""
    return self.music_playing       # Add this line to return the value of music_playing attribute when this function is called.
