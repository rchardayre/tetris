import pyglet
from pyglet.window import key
import config
import random
import time 
import pieces
from numpy import *

COLOR_ARRAY = [[75, 75, 75], [255, 0, 0], [0, 0, 255], [255, 255, 0], [255, 0, 255], [0, 255, 255], [0, 255, 0], [255, 255, 255]]
GAME_OVER = 1

class Grid:

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.start_pos = [height-2, round(width/2) - 1]
        self.grid = [ [ 0 for i in range(width) ] for j in range(height) ]
        self.BLOCK_LIST = [ FilledSquare(config.block_width, config.block_height, COLOR_ARRAY[0])
        , FilledSquare(config.block_width, config.block_height, COLOR_ARRAY[1])
        , FilledSquare(config.block_width, config.block_height, COLOR_ARRAY[2])
        , FilledSquare(config.block_width, config.block_height, COLOR_ARRAY[3])
        , FilledSquare(config.block_width, config.block_height, COLOR_ARRAY[4])
        , FilledSquare(config.block_width, config.block_height, COLOR_ARRAY[5])
        , FilledSquare(config.block_width, config.block_height, COLOR_ARRAY[6])
        , FilledSquare(config.block_width, config.block_height, COLOR_ARRAY[7]) ] 
       
        self.score = 0

        self.objectGrid = [ [ self.BLOCK_LIST[0] for i in range(width) ] for j in range(height) ]
        self.curr_piece = pieces.Piece(self.grid, self.start_pos)
        self.updateGrid()

    def updateGrid(self):
        #self.grid = grid
        #posx = random.randint(0,9)
        #posy = random.randint(0, 21)
        #value = random.randint(0,7)
        #self.grid[posx][posy] = [value, False]
        for row in range(0, self.width):
            for col in range(0, self.height):
                self.objectGrid[col][row] = self.BLOCK_LIST[self.grid[col][row]]
        
    def clock_update(self):
        if (self.curr_piece.move_piece(0, -1) == pieces.FORBIDDEN_MOVE):
            score = 0
            for row in self.grid[:]:
                if (0 not in row):
                    self.grid.remove(row)
                    self.grid.append([0 for i in range(self.width)])
                    score = (score + 5)*2 
            self.score = self.score + score
            if self.grid[self.start_pos[0]][self.start_pos[1]] != 0:
                return GAME_OVER;
            self.curr_piece = pieces.Piece(self.grid, self.start_pos)
        self.updateGrid()

    def key_pressed(self, symb, mod):
        if symb == key.LEFT:
            print("moving left")
            self.curr_piece.move_piece(-1, 0)
            self.updateGrid()
        elif symb == key.RIGHT:
            print("moving right")
            self.curr_piece.move_piece(1, 0)
            self.updateGrid()
        elif symb == key.UP:
            has_reached_bottom = False
            while(not has_reached_bottom):
                has_reached_bottom = (pieces.FORBIDDEN_MOVE == self.curr_piece.move_piece(0, -1))
            self.updateGrid()
        elif symb == key.DOWN:
            self.curr_piece.move_piece(0, -1)
            self.updateGrid()
        elif symb == key.E:
            self.curr_piece.rotate(pieces.ROTATE_CLOCKWISE)
            self.updateGrid()
        elif symb == key.R:
            self.curr_piece.rotate(pieces.ROTATE_COUNTERCLOCKWISE)
            self.updateGrid()
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

