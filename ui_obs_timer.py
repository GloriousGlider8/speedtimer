import pygame as pg
import lib.timing as tm
import lib.audio as aud
from tkinter import filedialog as fd
import sys
import json
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from pygame.locals import KEYDOWN, K_RETURN, K_BACKSPACE, MOUSEBUTTONDOWN, MOUSEMOTION

pg.display.init()
pg.font.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
BACKGROUND_COLOR = (46, 46, 46)
FOREGROUND_COLOR = (255, 255, 255)
SCROLLBAR_COLOR = (100, 100, 100)
SCROLLBAR_THUMB_COLOR = (150, 150, 150)
SEARCH_BAR_COLOR = (60, 60, 60)
SEARCH_TEXT_COLOR = (200, 200, 200)

def choose_font():
    # Create a Pygame screen
    screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pg.display.set_caption("Choose a Font")

    # Get list of available fonts
    available_fonts = pg.font.get_fonts()

    # Set up fonts and sizes
    font_size = 24
    search_font = pg.font.Font(None, font_size)
    list_font = pg.font.Font(None, font_size)

    def draw_text(surface: pg.Surface, text, position, font_name, color=FOREGROUND_COLOR):
        try:
            font = pg.font.Font(pg.font.match_font(font_name), font_size)
        except:
            font = pg.font.Font(None, font_size)
        text_surface = font.render(text, True, color)
        return surface.blit(text_surface, position)

    def draw_scrollbar(surface, scroll_pos, max_scroll):
        scrollbar_width = 20
        scrollbar_x = SCREEN_WIDTH - scrollbar_width
        scrollbar_height = SCREEN_HEIGHT - 40
        scrollbar_y = 20 + int((scroll_pos / max_scroll) * (scrollbar_height - scrollbar_width))

        # Draw the scrollbar background
        pg.draw.rect(surface, SCROLLBAR_COLOR, (scrollbar_x, 20, scrollbar_width, scrollbar_height))

        # Draw the scrollbar thumb
        pg.draw.rect(surface, SCROLLBAR_THUMB_COLOR, (scrollbar_x, scrollbar_y, scrollbar_width, scrollbar_width))

    def draw_search_bar(surface, text):
        search_bar_rect = pg.Rect(10, 50, SCREEN_WIDTH - 30, 30)
        pg.draw.rect(surface, SEARCH_BAR_COLOR, search_bar_rect)
        search_surface = search_font.render(text if text and text != "" else "Type and press ENTER to search", True, SEARCH_TEXT_COLOR)
        surface.blit(search_surface, (search_bar_rect.x + 5, search_bar_rect.y + 5))

    def get_visible_fonts(scroll_pos, screen_height, font_list):
        visible_fonts = []
        for i, font_name in enumerate(font_list):
            font_y = 50 + i * 30 - scroll_pos
            if 50 <= font_y <= screen_height - 60:
                visible_fonts.append((font_name, font_y + 30))
        return visible_fonts

    def scroll_to_position(mouse_y, scrollbar_height, thumb_height, max_scroll):
        return min(max(0, mouse_y - thumb_height // 2), max_scroll)

    running = True
    selected_font = None
    scroll_pos = 0
    max_scroll = len(available_fonts) * 30 - SCREEN_HEIGHT + 100
    search_text = ""
    filtered_fonts = available_fonts.copy()
    scrollbar_dragging = False

    while running:
        screen.fill(BACKGROUND_COLOR)
        
        draw_text(screen, "Choose a font.", (10, 10), None, (0, 105, 157))
        CUSTOM_FONT_BOUNDS = draw_text(screen, "Click here to use a custom file.", (10, 30), None, (0, 170, 255))
        
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    running = False
                elif event.key == K_BACKSPACE:
                    search_text = search_text[:-1]
                elif event.key == K_RETURN:
                    filtered_fonts = [f for f in available_fonts if search_text.lower() in f.lower()]
                else:
                    search_text += event.unicode
            elif event.type == MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if SCREEN_WIDTH - 20 <= mouse_pos[0] <= SCREEN_WIDTH and 20 <= mouse_pos[1] <= SCREEN_HEIGHT - 20:
                    thumb_rect = pg.Rect(SCREEN_WIDTH - 20, 20 + int((scroll_pos / max_scroll) * (SCREEN_HEIGHT - 60)), 20, 20)
                    if thumb_rect.collidepoint(mouse_pos):
                        scrollbar_dragging = True
                        drag_start_y = mouse_pos[1]
                        drag_start_scroll = scroll_pos
                elif CUSTOM_FONT_BOUNDS.collidepoint(mouse_pos[0], mouse_pos[1]):
                    Tk().withdraw()
                    font_path = askopenfilename(filetypes=[("TrueType Font", "*.ttf")])
                    if font_path:
                        selected_font = font_path
                        running = False
                else:
                    for font_name, font_y in get_visible_fonts(scroll_pos, SCREEN_HEIGHT, filtered_fonts):
                        if 10 <= mouse_pos[0] <= SCREEN_WIDTH - 30 and font_y <= mouse_pos[1] <= font_y + 30:
                            selected_font = font_name
                            running = False
            elif event.type == MOUSEMOTION and scrollbar_dragging:
                mouse_y = event.pos[1]
                thumb_height = 20
                scroll_pos = scroll_to_position(mouse_y, SCREEN_HEIGHT - 40, thumb_height, max_scroll)
            elif event.type == pg.MOUSEBUTTONUP:
                if event.button == 1:
                    scrollbar_dragging = False

        # Draw the search bar
        draw_search_bar(screen, search_text)

        # Draw font list with preview
        for font_name, font_y in get_visible_fonts(scroll_pos, SCREEN_HEIGHT, filtered_fonts):
            draw_text(screen, font_name, (10, font_y), font_name)

        # Draw the scrollbar
        draw_scrollbar(screen, scroll_pos, max_scroll)

        # Update display
        pg.display.flip()

    return selected_font

STD_FONT = pg.font.Font(size=16)

win = pg.display.set_mode((350, 480), pg.RESIZABLE)
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
                    win = pg.display.set_mode((350, 480), pg.RESIZABLE)
                case pg.K_RETURN:
                    if pg.key.get_mods() == 4097:
                        START = 0.5
                    else:
                        temp = fd.askopenfilename(title="Choose a target.", initialdir="./targets", filetypes=(("Speedrun Desktop Target Files", "*.spdtarg"), ("All Files", "*")))
                        if temp:
                            with open(temp, "r") as selFile:
                                TARGET = json.load(selFile)
                        else:
                            TARGET = None
                case pg.K_z:
                    temp = fd.askopenfilename(title="Choose a background.", initialdir="Downloads", filetypes=(("Supported Image Files", "*.png;*.jpg;*.jpeg"), ("All Files", "*")))
                    if temp:
                        BGR_NAME = temp
                        BGR = pg.image.load(temp)
                    else:
                        BGR_NAME = None
                        BGR = None
                case pg.K_x:
                    temp = choose_font()
                    if temp:
                        STD_FONT = pg.font.Font(pg.font.match_font(temp), size=16)
                    else:
                        STD_FONT = pg.font.Font(size=16)
                    
        elif ev.type == pg.KEYUP:
            if ev.key == pg.K_RETURN:
                if pg.key.get_mods() == 4097 and START == 0.5:
                    START = 1
                else:
                    START = 0
    
    win.fill((46, 46, 46))
    
    if START == 0:
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
        win.blit(STD_FONT.render("• 6: Reset Dimensions (350x480)", True, (0, 255, 255)), (0, 200))
        win.blit(STD_FONT.render("Minimizing the window hides the overlay!", True, (255, 0, 0)), (0, 220))
        win.blit(STD_FONT.render("Instead, click off the window.", True, (255, 255, 0)), (0, 240))
        win.blit(STD_FONT.render("You can also resize the overlay in OBS.", True, (255, 255, 255)), (0, 260))
        win.blit(STD_FONT.render("Use the ENTER key to choose a target file.", True, (255, 255, 255)), (0, 280))
        win.blit(STD_FONT.render(TARGET["name"] + ": " + TARGET["category"] if TARGET else "No target file selected.", True, (0, 255, 0)), (0, 300))
        win.blit(STD_FONT.render("Use the Z key to choose a background.", True, (255, 255, 255)), (0, 320))
        win.blit(STD_FONT.render(BGR_NAME if BGR else "No background selected.", True, (0, 255, 0)), (0, 340))
        win.blit(STD_FONT.render("Use the X key to choose a font.", True, (255, 255, 255)), (0, 360))
        win.blit(STD_FONT.render("Use SHIFT + ENTER to start!", True, (255, 255, 255) if START == 0 else (255, 255, 0)), (0, 380))
    elif START == 1:
        if BGR:
            win.blit(BGR, (0, 0))
    else:
        if TARGET:
            win.blit(STD_FONT.render("Now, hold SHIFT and let go of ENTER.", True, (0, 255, 0)), (10, 10))
        else:
            win.blit(STD_FONT.render("No target selected", True, (255, 255, 0)), (10, 10))
            TARGET = 0
    
    pg.display.update()
    
pg.quit()
sys.exit()