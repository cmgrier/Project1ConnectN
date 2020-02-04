import math
import agent

###########################
# Alpha-Beta Search Agent #
###########################

class AlphaBetaAgent(agent.Agent):
    """Agent that uses alpha-beta search"""

    # Class constructor.
    #
    # PARAM [string] name:      the name of this player
    # PARAM [int]    max_depth: the maximum search depth
    def __init__(self, name, max_depth):
        super().__init__(name)
        # Max search depth
        self.max_depth = max_depth

    # Pick a column.
    #
    # PARAM [board.Board] brd: the current board state
    # RETURN [int]: the column where the token must be added
    #
    # NOTE: make sure the column is legal, or you'll lose the game.
    def go(self, brd):
        """Search for the best move (choice of column for the token)"""
        # Your code here

    #Gives a score to a supplied board state
    #
    #PARAM [board.Board] brd: the board state to evaluate
    #RETURN [int]: the score of the board
    def score_board(self, brd):
        """Scores the given board according to benchmarks"""
        #TODO Implement Function
        #total points equal distance from the center, with token values increasing the closer they are to the center
        p1_center_priority = 0
        p2_center_priority = 0
        center_h = int((brd.h/2)-1)
        center_w = int((brd.w/2)-1)

    def within_boundaries(self,brd, h, w):
        """
        Checks if the cell is within the grid's boundaries
        :param h: height coordinate of the cell
        :param w: width coordinate of the cell
        :return: True if the cell is within the grid
        """
        if h >=  brd.h or h < 0:
            return False
        elif w >= brd.w or w < 0:
            return False
        else:
            return True

     def get_ranged_neighbors(brd, h, w, range):
         """
         Gets the 8 neighbors of a cell from a set distance
         :param h: height coordinate of the cell
         :param w: width coordinate of the cell
         :param range: the distance of the neighbors from the cell
         :return: list of cell values
         """


    # Get the successors of the given board.
    #
    # PARAM [board.Board] brd: the board state
    # RETURN [list of (board.Board, int)]: a list of the successor boards,
    #                                      along with the column where the last
    #                                      token was added in it
    def get_successors(self, brd):
        """Returns the reachable boards from the given board brd. The return value is a tuple (new board state, column number where last token was added)."""
        # Get possible actions
        freecols = brd.free_cols()
        # Are there legal actions left?
        if not freecols:
            return []
        # Make a list of the new boards along with the corresponding actions
        succ = []
        for col in freecols:
            # Clone the original board
            nb = brd.copy()
            # Add a token to the new board
            # (This internally changes nb.player, check the method definition!)
            nb.add_token(col)
            # Add board to list of successors
            succ.append((nb,col))
        return succ
