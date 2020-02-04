import math
import agent
from ConnectN.board import Board #TODO DELETE
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
        center_h = (brd.h//2)
        center_w = (brd.w//2)
        max_points = (brd.h+brd.w)//2
        print(center_h,",",center_w)
        print(max_points)
        range = 0
        neighbors = [1]
        while len(neighbors) > 0:
            neighbors = self.get_ranged_neighbors(brd,center_h,center_w,range)
            for token in neighbors:
                if brd.board[token[0]][token[1]] == 1:
                    p1_center_priority += max_points - int(range*1.51)
                elif brd.board[token[0]][token[1]] == 2:
                    p2_center_priority += max_points - int(range*1.5)
            range += 1
        return (p1_center_priority,p2_center_priority)

    def within_boundaries(self, brd, h, w):
        """
        Checks if the cell is within the grid's boundaries
        :param h: height coordinate of the cell
        :param w: width coordinate of the cell
        :return: True if the cell is within the grid
        """
        if h >= brd.h or h < 0:
            return False
        elif w >= brd.w or w < 0:
            return False
        else:
            return True

    def get_ranged_neighbors(self, brd, h, w, dist):
        """
        Gets the 8 neighbors of a cell from a set distance
        :param brd: the game board
        :param h: height coordinate of the cell
        :param w: width coordinate of the cell
        :param dist: the distance of the neighbors from the cell
        :return: list of valid cell coords
        """
        neighbors = set([])
        if dist == 0 and self.within_boundaries(brd, h, w):
            neighbors.add((h,w))
            return neighbors
        TL = (h-dist,w-dist)
        TR = (h-dist,w+dist)
        BL = (h+dist,w-dist)
        BR = (h+dist,w+dist)
        leftSide = BL[0]-TL[0] + 1
        rightSide = BR[0]-TR[0] + 1
        topSide = TR[1]-TL[1] + 1
        bottomSide = BR[1]-BL[1] + 1
        for height in range(leftSide):
            if self.within_boundaries(brd,TL[0]+height,TL[1]):
                neighbors.add((TL[0]+height,TL[1]))
        for height in range(rightSide):
            if self.within_boundaries(brd, TR[0] + height, TR[1]):
                neighbors.add((TR[0] + height, TR[1]))
        for width in range(topSide):
            if self.within_boundaries(brd,TL[0],TL[1]+width):
                neighbors.add((TL[0],TL[1]+width))
        for width in range(bottomSide):
            if self.within_boundaries(brd, BL[0], BL[1]+width):
                neighbors.add((BL[0], BL[1]+width))
        return neighbors


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


if __name__=="__main__":
    board = [
        [0,0,0,0,0,0],
        [0,2,0,1,0,0],
        [0,2,1,1,0,2],
        [0,1,1,2,0,1],
        [2,2,1,2,0,2]
    ]
    test = Board(board,6,5,4)
    abs = AlphaBetaAgent("srtidd",4)
    print(abs.score_board(test))