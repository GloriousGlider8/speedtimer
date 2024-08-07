import pygame

class AudioPlayer:
    """PyPlay AudioPlayer Class"""
    def __init__(self):
        pygame.init()
        pygame.mixer.init()

    def load(self, file):
        pygame.mixer.music.load(file)

    def play(self, loops=0, fade=0):
        pygame.mixer.music.play(loops, 0, fade)

    def pause(self):
        pygame.mixer.music.pause()

    def unpause(self):
        pygame.mixer.music.unpause()

    def stop(self):
        pygame.mixer.music.stop()
        
    def fade(self, fade):
        pygame.mixer.music.fadeout(fade)
    
    def jump(self, time, loops=0, fade=0):
        pygame.mixer.music.stop()
        pygame.mixer.music.play(loops, time, fade)
    
    def unload(self):
        pygame.mixer.music.unload()
        
    def queue(self, file, loops=0):
        pygame.mixer.music.queue(file, loops=loops)