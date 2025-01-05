import pygame
from pygame.locals import *
from Constants import *
from Graphics_Helpers import Graphic_Helpers
import os


class Graphics:
    def __init__(self, board, color, controller):
        flags = DOUBLEBUF
        self.screen = pygame.display.set_mode(SCREEN_SIZE, flags)
        self.board = board
        self.clock = pygame.time.Clock()
        self.color = color

        pygame.display.set_caption('Chess AI | Amit Sarussi')
        icon = pygame.image.load(ICON)
        pygame.display.set_icon(icon)
        os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

        pygame.font.init()
        self.font = pygame.font.Font(CHESS_COM_FONT, 24)

        self.GH = Graphic_Helpers(self.screen, self.board, self.font, self.color, controller)
        self.selected_square = None
        self.is_holding = False
        
        self.screen.set_alpha(None)
        
    
    def start(self):
        pygame.mixer.pre_init(44100, -16, 2, 512)
        pygame.init()
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.GH.mouse_down(pygame.mouse.get_pos())
                    
                if event.type == pygame.MOUSEBUTTONUP:
                    self.GH.mouse_up(pygame.mouse.get_pos())
                    
                if event.type == pygame.MOUSEMOTION:
                    self.GH.on_mouse_move(pygame.mouse.get_pos())
                
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                    
            self.dt = self.clock.tick(FRAME_RATE)  # Milliseconds since last frame
            self.update()

    def update(self):
        # Fill the screen with white
        self.screen.fill((255, 255, 255))
        
        self.GH.draw_board_squares()
        self.GH.draw_hold_indicator()
        self.GH.draw_board_coordinates()
        self.GH.draw_selected_square()
        self.GH.draw_last_move_square()
        self.GH.draw_board_pieces()
        self.GH.draw_held_piece()
        self.GH.draw_promotion_panel()
        
        self.GH.update_cursor()
        
        if SHOW_FPS:
            self.GH.draw_fps(self.clock.get_fps())
        
        
        # Update the display
        pygame.display.flip()

    
    
