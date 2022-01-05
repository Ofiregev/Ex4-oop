import pygame
from pygame import RESIZABLE


class g:
    def __init__(self):
        pygame.init()
        video_infos = pygame.display.Info()
        WIDTH, HIGHT = video_infos.current_w, video_infos.current_h - 50
        self.screen = pygame.display.set_mode((WIDTH, HIGHT), depth=32, flags=RESIZABLE)
g()