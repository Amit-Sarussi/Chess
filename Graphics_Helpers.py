from math import e
import pygame
from Board import Board
from Constants import *

class Graphic_Helpers:
    def __init__(self, screen, board: Board, font, color, controller):
        self.board = board
        self.color = color
        self.controller = controller
        self.font = font
        self.hover_square = (0, 0)
        self.image_cache = {}
        self.is_holding = False
        self.last_move = None
        self.mouse_pos = (0, 0)
        self.screen = screen
        self.select_promotion_state = False
        self.selected_square = None
    
    def load_piece_image(self, piece):
        # Check if the piece image is already cached
        piece_filename = f"{PIECES_DIR}{piece.piece_to_filename()}.png"
        if piece_filename not in self.image_cache:
            # If not cached, load and store it in the cache
            piece_surface = pygame.image.load(piece_filename)
            piece_surface = piece_surface.convert_alpha()
            piece_surface = pygame.transform.smoothscale(piece_surface, PIECE_SIZE)
            self.image_cache[piece_filename] = piece_surface
        return self.image_cache[piece_filename]
            
    def draw_board_squares(self):
        w, h = self.screen.get_size()
        for i in range(8):
            for j in range(8):
                square = pygame.Rect(j * w / 8, i * h / 8, w / 8, h / 8)
                color = LIGHT_SQUARE_COLOR if (i + j) % 2 == 0 else DARK_SQUARE_COLOR
                pygame.draw.rect(self.screen, color, square)
    
    def draw_selected_square(self):
        if self.selected_square is not None:
            w, h = self.screen.get_size()
            if self.color == 'w':
                y, x = self.selected_square
            else:
                y = 7 - self.selected_square[0]
                x = 7 - self.selected_square[1]
            s = pygame.Surface((w / 8, h / 8))  # the size of your rect
            s.set_alpha(128)                # alpha level
            s.fill(SELECTED_SQUARE_COLOR)           # this fills the entire surface
            self.screen.blit(s, (x * w / 8,y * h / 8))
    
    def draw_last_move_square(self):
        if self.last_move is not None:
            w, h = self.screen.get_size()
            if self.color == 'w':
                y1, x1 = self.last_move[0]
                y2, x2 = self.last_move[1]
            else:
                y1 = 7 - self.last_move[0][0]
                x1 = 7 - self.last_move[0][1]
                y2 = 7 - self.last_move[1][0]
                x2 = 7 - self.last_move[1][1]
            
            # Draw start square
            s = pygame.Surface((w / 8, h / 8))  # the size of your rect
            s.set_alpha(128)                # alpha level
            s.fill(SELECTED_SQUARE_COLOR)           # this fills the entire surface
            self.screen.blit(s, (x1 * w / 8,y1 * h / 8))
            
            # Draw end square
            s = pygame.Surface((w / 8, h / 8))  # the size of your rect
            s.set_alpha(128)                # alpha level
            s.fill(SELECTED_SQUARE_COLOR)           # this fills the entire surface
            self.screen.blit(s, (x2 * w / 8,y2 * h / 8))
    
    def draw_hold_indicator(self):
        if self.is_holding:
            w, h = self.screen.get_size()
            if self.color == 'w':
                y, x = self.hover_square
            else:
                y = 7 - self.hover_square[0]
                x = 7 - self.hover_square[1]
            s = pygame.Surface((w / 8, h / 8), pygame.SRCALPHA)  # the size of your rect
            s.set_alpha(128)
            s.fill((0, 0, 0, 0))  # fill with transparent color
            pygame.draw.rect(s, HOLD_INDICATOR_COLOR, s.get_rect(), 8)  # draw border
            self.screen.blit(s, (x * w / 8, y * h / 8))

    
    def draw_board_coordinates(self):
        w, h = self.screen.get_size()
        padding_x = SCREEN_SIZE[0] / (8 * 13)
        padding_y = SCREEN_SIZE[1] / (8 * 13)
        
        # Numbers
        for i in range(8):
            text = str(8 - i)
            text_surface = self.font.render(text, True, DARK_SQUARE_COLOR if (i) % 2 == 0 else LIGHT_SQUARE_COLOR)
            self.screen.blit(text_surface, (padding_x, padding_y + i * h / 8))
        
        # Letters
        for i in range(8):
            if self.color == 'w':
                text = chr(ord('a') + i)
            else:
                text = chr(ord('h') - i)
            text_surface = self.font.render(text, True, DARK_SQUARE_COLOR if (i) % 2 == 1 else LIGHT_SQUARE_COLOR)
            self.screen.blit(text_surface, (w / 8 - padding_x - 16 + i * w / 8, h - padding_y - 24))
    
    def draw_board_pieces(self):
        w, h = self.screen.get_size()
        for i in range(8):
            for j in range(8):
                if self.color == 'w':
                    piece = self.board.board[i, j]
                    if self.selected_square is not None and i == self.selected_square[0] and j == self.selected_square[1] and self.is_holding: continue
                else:
                    piece = self.board.board[7 - i, 7 - j]
                    if self.selected_square is not None and 7 - i == self.selected_square[0] and 7 - j == self.selected_square[1] and self.is_holding: continue
                if piece is not None:
                    piece_surface = self.load_piece_image(piece)  # Use the cached image
                    self.screen.blit(piece_surface, (j * w / 8 + (w/8 - PIECE_SIZE[0])/2, i * h / 8 + (h/8 - PIECE_SIZE[1])/2))
                    
    def update_cursor(self):
        w, h = self.screen.get_size()
        mouse_pos = pygame.mouse.get_pos()
        square_pos = (int(mouse_pos[1] // (h / 8)), int(mouse_pos[0] // (w / 8)))
        if self.board.is_within_bounds(square_pos):
            piece = self.board.board[square_pos]
            if piece is not None and piece.color == self.color:
                pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_HAND)
            else:
                pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_ARROW)
    

    def draw_promotion_panel(self):
        if self.select_promotion_state:
            w, h = self.screen.get_size()
            s = pygame.Surface((w, h), pygame.SRCALPHA)
    
    def select_square(self, square):
        if self.color == 'w':
            self.selected_square = square
        else:
            self.selected_square = (7 - square[0], 7 - square[1])
    
    def draw_held_piece(self):
        if self.is_holding:
            w, h = self.screen.get_size()
            i, j = self.selected_square
            x, y = self.mouse_pos
            if self.color == 'b':
                i = 7 - i
                j = 7 - j
                x = 7 - x
                y = 7 - y
            piece = self.board.board[self.selected_square]
            piece_surface = self.load_piece_image(piece)
            self.screen.blit(piece_surface, (x + (w/8 - PIECE_SIZE[0])/2 - w/16, y + (h/8 - PIECE_SIZE[1])/2 - h/16))
    
    def draw_fps(self, fps):
        text = self.font.render(f"FPS: {int(fps)}", True, (0, 0, 0))
        self.screen.blit(text, (10, 10))
        
                    
    def mouse_down(self, mouse_pos):
        square = (int(mouse_pos[1] // (SCREEN_SIZE[1] / 8)), int(mouse_pos[0] // (SCREEN_SIZE[0] / 8)))
        piece = self.board.board[square]
        self.is_holding = self.board.is_within_bounds(square) and piece is not None and piece.color == self.color
        if self.is_holding:
            self.select_square(square)
        else:
            self.selected_square = None
        
    def mouse_up(self, mouse_pos):
        if not self.is_holding: return
        self.is_holding = False
        
        current_square = (int(mouse_pos[1] // (SCREEN_SIZE[1] / 8)), int(mouse_pos[0] // (SCREEN_SIZE[0] / 8)))
        move = (self.selected_square, current_square)
        
        if move[0] == move[1]:
            return
        
        self.selected_square = None
        self.last_move = move

        # Is promotion?
        if self.select_promotion_state == False and self.board.is_move_promotion(move):
            self.select_promotion_state = True
            return
        
        if self.select_promotion_state:
            self.select_promotion_state = False
            result = self.controller.make_move(move, promotion="q")
            if result:
                self.last_move = result[1]
            else:
                self.last_move = None
            return
        
        
        result = self.controller.make_move(move)
        if result:
            self.last_move = result[1]
        else:
            self.last_move = None
        
    def on_mouse_move(self, mouse_pos):
        """
        Handle the mouse movement event and update the hover square.
        """
        
        square = (int(mouse_pos[1] // (SCREEN_SIZE[1] / 8)), int(mouse_pos[0] // (SCREEN_SIZE[0] / 8)))
        if square[0] >= 0 and square[0] < 8 and square[1] >= 0 and square[1] < 8:
            if self.color == 'w':
                self.hover_square = square
            else:
                self.hover_square = (7 - square[0], 7 - square[1])
                
        self.mouse_pos = mouse_pos