import config

SQUARE_PIECE = 1
BAR_PIECE = 2
L_PIECE = 3
J_PIECE = 4
T_PIECE = 5
S_PIECE = 6
Z_PIECE = 7

PIECE_LIST = [SQUARE_PIECE, BAR_PIECE, L_PIECE, J_PIECE, T_PIECE, S_PIECE, Z_PIECE]
ROTATE_0 = 0
ROTATE_90 = 1
ROTATE_180 = 2
ROTATE_270 = 3

ALLOWED_MOVE = 0
FORBIDDEN_MOVE = 1

ROTATE_CLOCKWISE = 0
ROTATE_COUNTERCLOCKWISE = 1

PIECE_SHIFT_LIST = [
            [  [],
               [[0,0],[0,1],[1,0],[1,1]], #SQUARE      ##
#                                                      X#

               [[0,0],[0,-1],[0,1],[0,2]], #BAR      #X##

               [[0,0],[0,-1],[0,1],[1,1]], #L          #
                                                     #X#

               [[0,0],[1,-1],[0,-1],[0,1]], #J       #
                                                     #X#

               [[0,0],[0,-1],[0,1],[1,0]], #T         # 
                                                     #X#

               [[0,0],[0,-1],[1,0],[1,1]], #S        ##
                                                    #X

               [[0,0],[1,0],[1,-1],[0,1]] #Z        ##
#                                                    X#
            ],
            [  [],
               [[0,0],[0,1],[1,0],[1,1]], #SQUARE    ##
#                                                    X#

               [[1,1],[0,1],[-2,1],[-1,1]], #BAR      #
#                                                    X#
                                                      #
                                                      #

               [[0,0],[1,0],[-1,0],[-1,1]], #L        #
#                                                     X
                                                      ##

               [[0,0],[1,0],[1,1],[-1,0]],  #J        ##
#                                                     X
                                                      #

               [[0,0],[1,0],[-1,0],[0,1]], #T         #
#                                                     X#
                                                      #

               [[0,0],[0,1],[1,0],[-1,1]], #S         #
#                                                     X#
                                                       #

               [[0,0],[1,1],[0,1],[-1,0]] #Z           #
#                                                     X#
                                                      #
            ],
            [  [],
               [[0,0],[0,1],[1,0],[1,1]], #SQUARE       ##
#                                                       X#

               [[-1,0],[-1,-1],[-1,1],[-1,2]], #BAR    ####
#                                                       X

               [[0,0],[0,-1],[-1,-1],[0,1]], #L        #X#
                                                       #

               [[0,0],[0,-1],[0,1],[-1,1]], #J           #X#
                                                           #

               [[0,0],[0,-1],[0,1],[-1,0]], #T          #X#
                                                         #

               [[0,0],[0,-1],[1,0],[1,1]], #S          ##
                                                      #X

               [[0,0],[1,0],[1,-1],[0,1]] #Z         ##
#                                                     X#
            ],
            [  [],
               [[0,0],[0,1],[1,0],[1,1]], #SQUARE     ##
#                                                     X#

               [[-1,-1],[-2,-1],[0,-1],[1,-1]], #BAR     #
                                                         #X
                                                         #
                                                         #

               [[0,0],[1,0],[1,-1],[-1,0]], #L       ##
#                                                     X
                                                      #

               [[0,0],[1,0],[-1,0],[-1,-1]], #J       #
#                                                     X
                                                     ##

               [[0,0],[0,-1],[1,0],[-1,0]], #T       #
                                                    #X
                                                     #

               [[0,0],[0,1],[1,0],[-1,1]], #S        #
#                                                    X#
                                                      #

               [[0,0],[1,1],[-1,0],[0,1]] #Z          #
#                                                    X#
                                                     #
            ]
            ]

class Piece():
    def __init__(self, grid, value):
        self.grid = grid

    def __init__(self, grid, start_pos, form_idx):
        self.grid = grid
        self.form = form_idx
        self.rotateState = 0 
        self.position = [start_pos[0], start_pos[1]]
        for shift in PIECE_SHIFT_LIST[self.rotateState][self.form]:
            blockpos = [start_pos[0]+shift[0], start_pos[1]+shift[1]]
            self.grid[blockpos[0]][blockpos[1]] = self.form
    
    def move_piece(self, shift_x, shift_y):
        if self.is_move_allowed(self.rotateState, shift_x, shift_y) == FORBIDDEN_MOVE:
            return FORBIDDEN_MOVE

        self.update_position(self.rotateState, shift_x, shift_y)

        return ALLOWED_MOVE

    def rotate(self, orientation):
        if(orientation == ROTATE_CLOCKWISE):
            rotateIdx = (self.rotateState + 1)%4
        else:
            rotateIdx = (self.rotateState - 1)%4
        
        if self.is_move_allowed(rotateIdx, 0, 0) == FORBIDDEN_MOVE:
            return FORBIDDEN_MOVE
        
        self.update_position(rotateIdx, 0, 0)
        
        self.rotateState = rotateIdx

        return ALLOWED_MOVE

    def is_move_allowed(self, rotateIdx, shift_x, shift_y):
        listPosition = [[shift[0] + self.position[0], shift[1] + self.position[1]] for shift in PIECE_SHIFT_LIST[self.rotateState][self.form]]
        for shift in PIECE_SHIFT_LIST[rotateIdx][self.form]:
            new_y = self.position[0] + shift[0] + shift_y
            new_x = self.position[1] + shift[1] + shift_x
            if  (
                    (new_y < 0) or (new_x < 0) or
                    (new_x >= config.nb_block_horizontal) or
                    (self.grid[new_y][new_x] != 0 and ([new_y, new_x] not in listPosition))
                ):
                return FORBIDDEN_MOVE
        return ALLOWED_MOVE

    def update_position(self, rotateIdx, shift_x, shift_y):
        ##Delete prev position
        for shift in PIECE_SHIFT_LIST[self.rotateState][self.form]:
            posy = shift[0] + self.position[0]
            posx = shift[1] + self.position[1]
            self.grid[posy][posx] = 0

        ##Update new position
        for shift in PIECE_SHIFT_LIST[rotateIdx][self.form]:
            posy = shift[0] + self.position[0] + shift_y
            posx = shift[1] + self.position[1] + shift_x
            self.grid[posy][posx] = self.form

        self.position[0] = self.position[0] + shift_y
        self.position[1] = self.position[1] + shift_x
