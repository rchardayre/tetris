import pyglet
from pyglet.window import key
import config
import random
import sys
import time 
import pieces
from numpy import *

COLOR_ARRAY = [[75, 75, 75], [255, 0, 0], [0, 0, 255], [255, 255, 0], [255, 0, 255], [0, 255, 255], [0, 255, 0], [255, 255, 255]]
GAME_OVER = 1


class Grid:

    def __init__(self, width, height, record):
        self.width = width
        self.height = height
        self.start_pos = [height-2, round(width/2) - 1]
        self.grid = [ [ 0 for i in range(width) ] for j in range(height) ]
        if not config.is_simulation:
            self.BLOCK_LIST = [ FilledSquare(config.block_width, config.block_height, COLOR_ARRAY[0])
        , FilledSquare(config.block_width, config.block_height, COLOR_ARRAY[1])
        , FilledSquare(config.block_width, config.block_height, COLOR_ARRAY[2])
        , FilledSquare(config.block_width, config.block_height, COLOR_ARRAY[3])
        , FilledSquare(config.block_width, config.block_height, COLOR_ARRAY[4])
        , FilledSquare(config.block_width, config.block_height, COLOR_ARRAY[5])
        , FilledSquare(config.block_width, config.block_height, COLOR_ARRAY[6])
        , FilledSquare(config.block_width, config.block_height, COLOR_ARRAY[7]) ] 
       
            self.objectGrid = [ [ self.BLOCK_LIST[0] for i in range(width) ] for j in range(height) ]
        self.score = 0
        self.record = record
        self.list_form_idx = 0
        
        self.curr_move_list = []
        self.curr_piece = pieces.Piece(self.grid, self.start_pos, self.getNextForm())
        self.updateGrid()

    def getNextForm(self):
        if config.is_replay:
            if len(self.record['forms']) > self.list_form_idx:
                form_idx = self.record['forms'][self.list_form_idx]
                self.list_form_idx = self.list_form_idx + 1
            else:
                print("NO MORE FORMS")
                sys.exit(1)
        else:
            form_idx = int(random.choice(pieces.PIECE_LIST))
            if config.is_record:
                self.record['forms'].append(form_idx)

        return form_idx

    def updateGrid(self):
        if not config.is_simulation:
            for row in range(0, self.width):
                for col in range(0, self.height):
                    self.objectGrid[col][row] = self.BLOCK_LIST[self.grid[col][row]]
        
    def clock_update(self):
        if config.is_record:
            self.record['moves'].append(self.curr_move_list)
            self.curr_move_list = []
        if (self.curr_piece.move_piece(0, -1) == pieces.FORBIDDEN_MOVE):
            score = 0
            for row in self.grid[:]:
                if (0 not in row):
                    self.grid.remove(row)
                    self.grid.append([0 for i in range(self.width)])
                    score = (score + 5)*2 
            self.score = self.score + score
            if self.grid[self.start_pos[0]][self.start_pos[1]] != 0:
                return GAME_OVER

            self.curr_piece = pieces.Piece(self.grid, self.start_pos, self.getNextForm())

        self.updateGrid()

    def move_left(self):
        if config.is_record:
            self.curr_move_list.append("L")
        self.curr_piece.move_piece(-1, 0)
        self.updateGrid()

    def move_right(self):
        if config.is_record:
            self.curr_move_list.append("R")
        self.curr_piece.move_piece(1, 0)
        self.updateGrid()

    def move_down(self):
        if config.is_record:
            self.curr_move_list.append("D")
        self.curr_piece.move_piece(0, -1)
        self.updateGrid()

    def hard_drop(self):
        if config.is_record:
            self.curr_move_list.append("H")
        has_reached_bottom = False
        while(not has_reached_bottom):
            has_reached_bottom = (pieces.FORBIDDEN_MOVE == self.curr_piece.move_piece(0, -1))
        self.updateGrid()
   
    def rotate_clockwise(self):
        if config.is_record:
            self.curr_move_list.append("T")
        self.curr_piece.rotate(pieces.ROTATE_CLOCKWISE)
        self.updateGrid()

    def rotate_counterclockwise(self):
        if config.is_record:
            self.curr_move_list.append("Y")
        self.curr_piece.rotate(pieces.ROTATE_COUNTERCLOCKWISE)
        self.updateGrid()

    def key_pressed(self, symb, mod):
        if symb == key.LEFT:
            self.move_left()
        elif symb == key.RIGHT:
            self.move_right()
        elif symb == key.UP:
            self.hard_drop()
        elif symb == key.DOWN:
            self.move_down()
        elif symb == key.E:
            self.rotate_clockwise()
        elif symb == key.R:
            self.rotate_counterclockwise()
        elif symb == key.P:
            self.pretty_print()

    def draw(self):  
        for row in range(0, self.width):
            for col in range(0, self.height):
                self.objectGrid[col][row].draw(80 + row*config.block_width, 100 + col*config.block_height)
        labelscore = pyglet.text.Label("%d" % self.score, font_name='Times New Roman', font_size=20, x=config.window_width-50, y = 50, anchor_x='center', anchor_y='center')
        labelscore.draw()

    def pretty_print(self):
        for row in reversed(self.grid):
            print(row)

class FilledSquare:
    def __init__(self, width, height, color):
        self.width = width
        self.height = height
        x = width/2.0
        y = height/2.0
        self.vlist = pyglet.graphics.vertex_list(4, ('v2f', [-x,-y, x,-y, -x,y, x,y]), ('t2f', [0,0, 1,0, 0,1, 1,1]), ('c3B',(color[0],color[1],color[2], color[0],color[1],color[2], color[0],color[1],color[2], color[0],color[1],color[2])))
    def draw(self, xpos, ypos):
        pyglet.gl.glPushMatrix()
        pyglet.gl.glTranslatef(xpos, ypos, 0)
        self.vlist.draw(pyglet.gl.GL_TRIANGLE_STRIP)        
        pyglet.gl.glPopMatrix()

