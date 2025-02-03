import pygame
from pygame.locals import *
from Constants import *
from Graphics_Helpers import Graphic_Helpers
import os

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

class Graphics:
    def __init__(self, board, color, controller=None, spectate_mode=False, GameViewer=None):
        flags = DOUBLEBUF
        self.screen = pygame.display.set_mode(SCREEN_SIZE, flags)
        self.board = board
        self.clock = pygame.time.Clock()
        self.color = color

        pygame.display.set_caption('Chess AI | Amit Sarussi')
        icon = pygame.image.load(ICON)
        pygame.display.set_icon(icon)

        pygame.font.init()
        self.font = pygame.font.Font(CHESS_COM_FONT, 24)

        self.GH = Graphic_Helpers(self.screen, self.board, self.font, self.color, controller)
        self.selected_square = None
        self.is_holding = False
        self.spectate = spectate_mode
        self.GV = GameViewer
        self.stopped_playing = False
        
        self.screen.set_alpha(None)

        if self.spectate:
            self.MOVEEVENT, t, trail = pygame.USEREVENT+1, self.GV.time_between, []
            pygame.time.set_timer(self.MOVEEVENT, t)
        
    
    def start(self):
        pygame.mixer.pre_init(44100, -16, 2, 512)
        pygame.init()
        
        while True:
            for event in pygame.event.get():
                if self.spectate == False:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        self.GH.mouse_down(pygame.mouse.get_pos())
                        
                    if event.type == pygame.MOUSEBUTTONUP:
                        self.GH.mouse_up(pygame.mouse.get_pos())
                        
                    if event.type == pygame.MOUSEMOTION:
                        self.GH.on_mouse_move(pygame.mouse.get_pos())
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_b:
                            self.GH.print_board_data()
                else:
                    if event.type == self.MOVEEVENT:
                        move = self.GV.make_next_move()
                        if move == None:
                            pygame.event.clear(self.MOVEEVENT)
                            self.GH.checkmate = self.GV.checkmate
                            self.stopped_playing = True
                        self.GH.last_move = move

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
        if self.stopped_playing == True or self.GH.checkmate is not None:
            self.GH.draw_checkmate_sign()
        self.GH.draw_held_piece()
        self.GH.draw_promotion_panel()
        
        self.GH.update_cursor()
        
        if SHOW_FPS:
            self.GH.draw_fps(self.clock.get_fps())
        
        # Update the display
        pygame.display.flip()

    
    
