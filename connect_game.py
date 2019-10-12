import math
import sys
from typing import Tuple

from pygame.gfxdraw import filled_circle, aacircle

from assets import *
from config import black, red, yellow
from game_data import GameData
from graphics import GameRenderer
from pygame import mixer

import pygame

class ConnectGame:
    game_data: GameData
    renderer: GameRenderer

    def __init__(self, game_data: GameData, renderer: GameRenderer):
        self.game_data = game_data
        self.renderer = renderer

        self.sq_size: int = 100

        self.width: int = 7 * self.sq_size
        self.height: int = 7 * self.sq_size
        self.size: Tuple[int, int] = (self.width, self.height)
        self.radius: int = int(self.sq_size / 2 - 5)

    def quit(self):
        sys.exit()

    def mouse_move(self, posx: int):
        # Queue message that mouse has been moved

        ### Renderer should see action is mouse move, and draw this ##########################
        pygame.draw.rect(self.renderer.screen, black, (0, 0, self.width, self.sq_size))
        if self.game_data.turn == 0:
            self.renderer.draw_red_coin(posx - (self.sq_size / 2), int(self.sq_size) - self.sq_size + 5)
        else:
            self.renderer.draw_yellow_coin(posx - (self.sq_size / 2), int(self.sq_size) - self.sq_size + 5)
        #######################################################################################
    def mouse_click(self, posx: int):
        ### Renderer should see action is mouse click, and draw this ##########################
        pygame.draw.rect(self.renderer.screen, black, (0, 0, self.width, self.sq_size))
        #######################################################################################
        if self.game_data.turn == 0:

            col: int = int(math.floor(posx / self.sq_size))

            if self.game_data.game_board.is_valid_location(col):
                row: int = self.game_data.game_board.get_next_open_row( col)

                self.game_data.last_move_row = row
                self.game_data.last_move_col = col
                self.game_data.game_board.drop_piece(row, col, 1)

            self.print_board()

            if self.game_data.game_board.winning_move(1):
                ### Move to renderer #########################
                self.renderer.label = self.renderer.myfont.render("PLAYER 1 WINS!", 1, red)
                self.renderer.screen.blit(self.renderer.label, (40, 10))
                ###############################################

                mixer.music.load(event_sound)
                mixer.music.play(0)
                self.game_data.game_over = True
            pygame.display.update()
        else:
            col: int = int(math.floor(posx / self.sq_size))

            if self.game_data.game_board.is_valid_location(col):
                row: int = self.game_data.game_board.get_next_open_row( col)

                self.game_data.last_move_row = row
                self.game_data.last_move_col = col
                self.game_data.game_board.drop_piece( row, col, 2)

            self.print_board()

            if self.game_data.game_board.winning_move( 2):
                ##### Move to renderer ###
                self.renderer.label = self.renderer.myfont.render("PLAYER 2 WINS!", 1, yellow)
                self.renderer.screen.blit(self.renderer.label, (40, 10))
                ##########################

                mixer.music.load(event_sound)
                mixer.music.play(0)
                self.game_data.game_over = True
            pygame.display.update()
        self.game_data.turn += 1
        self.game_data.turn = self.game_data.turn % 2

    def undo(self):
        self.game_data.game_board.drop_piece(
            self.game_data.last_move_row,
            self.game_data.last_move_col,
            0
        )

        ################## Move to Renderer #######################
        filled_circle(
            self.renderer.screen,
            self.game_data.last_move_row,
            self.game_data.last_move_col,
            self.radius,
            black
        )

        aacircle(
            self.renderer.screen,
            self.game_data.last_move_row,
            self.game_data.last_move_col,
            self.radius,
            black
        )

        self.renderer.draw_black_coin(
            self.game_data.last_move_col * self.sq_size + 5,
            self.height - (self.game_data.last_move_row * self.sq_size + self.sq_size - 5)
        )

        self.print_board()
        ############################################################
        self.game_data.turn += 1
        self.game_data.turn = self.game_data.turn % 2

    def update(self):
        pass

    def draw(self):
        self.renderer.draw(self.game_data)

    def print_board(self):
        self.game_data.game_board.print_board()