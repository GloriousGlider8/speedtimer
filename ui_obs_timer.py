import pygame as pg
import lib.timing as tm
import lib.audio as aud
from tkinter import filedialog as fd
import sys
import json

pg.display.init()
pg.font.init()

STD_FONT = pg.font.Font(size=16)

win = pg.display.set_mode((350, 720), pg.RESIZABLE)
pg.display.set_caption("Speedrun Desktop OBS Studio Overlay")

DO_RUN = True
TARGET = None
BGR = None
BGR_NAME = None
START = 0

while DO_RUN:
    for ev in pg.event.get():
        if ev.type == pg.QUIT:
            DO_RUN = False
        elif ev.type == pg.KEYDOWN:
            match ev.key:
                case pg.K_1:
                    win = pg.display.set_mode((win.get_width(), 480), pg.RESIZABLE)
                case pg.K_2:
                    win = pg.display.set_mode((win.get_width(), 720), pg.RESIZABLE)
                case pg.K_3:
                    win = pg.display.set_mode((win.get_width(), 1080), pg.RESIZABLE)
                case pg.K_4:
                    win = pg.display.set_mode((win.get_width(), 1440), pg.RESIZABLE)
                case pg.K_5:
                    win = pg.display.set_mode((win.get_width(), 2160), pg.RESIZABLE)
                case pg.K_6:
                    win = pg.display.set_mode((350, 720), pg.RESIZABLE)
                case pg.K_RETURN:
                    if pg.key.get_mods() == 4097:
                        START = 0.5
                    else:
                        temp = fd.askopenfilename(title="Choose a target.", initialdir="./targets", filetypes=(("Speedrun Desktop Target Files", "*.spdtarg"), ("All Files", "*")))
                        if temp:
                            with open(temp, "r") as selFile:
                                TARGET = json.load(selFile)
                case pg.K_z:
                    temp = fd.askopenfilename(title="Choose a background.", initialdir="Downloads", filetypes=(("Supported Image Files", "*.png;*.jpg;*.jpeg"), ("All Files", "*")))
                    if temp:
                        BGR_NAME = temp
                        BGR = pg.image.load(temp)
                    else:
                        BGR_NAME = None
                        BGR = None
                    
        elif ev.type == pg.KEYUP:
            if ev.key == pg.K_RETURN:
                if pg.key.get_mods() == 4097:
                    START = 1
                else:
                    START = 0
    
    win.fill((46, 46, 46))
    
    if START != 1:
        win.blit(STD_FONT.render("Use a Window Capture and choose:", True, (255, 255, 255)), (0, 0))
        win.blit(STD_FONT.render("[python.exe]: Speedrun Desktop OBS Studio Overlay", True, (255, 0, 255)), (0, 20))
        win.blit(STD_FONT.render("Resize the window to fit your OBS Overlay needs.", True, (255, 255, 255)), (0, 40))
        win.blit(STD_FONT.render(f"Current Size: {win.get_width()}x{win.get_height()}", True, (0, 255, 255)), (0, 60))
        win.blit(STD_FONT.render("Use the following keybinds to set dimensions.", True, (255, 255, 255)), (0, 80))
        win.blit(STD_FONT.render("• 1: Set height to 480 (480p)", True, (0, 255, 255)), (0, 100))
        win.blit(STD_FONT.render("• 2: Set height to 720 (720p)", True, (0, 255, 255)), (0, 120))
        win.blit(STD_FONT.render("• 3: Set height to 1080 (1080p)", True, (0, 255, 255)), (0, 140))
        win.blit(STD_FONT.render("• 4: Set height to 1440 (1440p)", True, (0, 255, 255)), (0, 160))
        win.blit(STD_FONT.render("• 5: Set height to 2160 (4k)", True, (0, 255, 255)), (0, 180))
        win.blit(STD_FONT.render("• 6: Reset Dimensions (350x720)", True, (0, 255, 255)), (0, 200))
        win.blit(STD_FONT.render("Minimizing the window hides the overlay!", True, (255, 0, 0)), (0, 220))
        win.blit(STD_FONT.render("Instead, click off the window.", True, (255, 255, 0)), (0, 240))
        win.blit(STD_FONT.render("You can also resize the overlay in OBS.", True, (255, 255, 255)), (0, 260))
        win.blit(STD_FONT.render("Use the ENTER key to choose a target file.", True, (255, 255, 255)), (0, 280))
        win.blit(STD_FONT.render(TARGET["name"] + ": " + TARGET["category"] if TARGET else "No target file selected.", True, (0, 255, 0)), (0, 300))
        win.blit(STD_FONT.render("Use the Z key to choose a background.", True, (255, 255, 255)), (0, 320))
        win.blit(STD_FONT.render(BGR_NAME if BGR else "No background selected.", True, (0, 255, 0)), (0, 340))
        win.blit(STD_FONT.render("Use SHIFT + ENTER to start!", True, (255, 255, 255) if START == 0 else (255, 255, 0)), (0, 360))
    else:
        win.blit(BGR, (0, 0))
    
    pg.display.update()
    
pg.quit()
sys.exit()