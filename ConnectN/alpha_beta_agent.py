import math
import agent
import board

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
        score = 0
        for r in range(0, brd.h):
            for c in range(0, brd.w):
                score += self.evaluate_token(brd, r, c)
        return score


    # Get the successors of the given board.
    #
    # PARAM [board.Board] brd: the board state
    # RETURN [list of (board.Board, int)]: a list of the successor boards,
    #                                      along with the column where the last
    #                                      token was added in it

    def evaluate_token(self, brd, r, c):
        token = brd.board[r][c]
        if token == 0:
            return 0
        t_power = 0
        for dir in range(0, 7):
            t_power += self.look_for_line(brd, r, c, dir)
        if self.player != token:
            return t_power * -1
        else:
            return t_power


    def look_for_line(self, brd, r, c, dir):
        """
        dir:
        3 0 1
        2 x 2
        1 0 3
        """
        ir = 0
        ic = 0
        if dir == 0:
            ir = -1
        if dir == 1:
            ir = -1
            ic = 1
        if dir == 2:
            ic = 1
        if dir == 3:
            ir = 1
            ic = 1

        origin = brd.board[r][c]
        if origin == 1:
            opponent = 2
        else:
            opponent = 1
        in_p_dir = 0
        p_open = 0
        blocked = False
        for i in range(0, brd.n):
            rx = r + ir * i
            cx = c + ic * i
            if 0 < rx < brd.h and 0 < cx < brd.w:
                token = brd.board[rx][cx]
                if token == origin and not blocked:
                    in_p_dir += 1
                elif token == opponent:
                    blocked = True
                elif not blocked:
                    p_open += 1
        in_n_dir = 0
        n_open = 0
        blocked = False
        for i in range(0, brd.n):
            rx = r - ir * i
            cx = c - ic * i
            if 0 < rx < brd.h and 0 < cx < brd.w:
                token = brd.board[rx][cx]
                if token == origin and not blocked:
                    in_p_dir += 1
                elif token == opponent:
                    blocked = True
                elif not blocked:
                    n_open += 1

        return in_p_dir + in_n_dir + .5 * (n_open + p_open)



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

if __name__ == '__main__':
    data = [[0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0]]
    board = board.Board(data, 7, 6, 4)
    aba = AlphaBetaAgent("abba", 2)
    aba.player = 1
    print(aba.score_board(board))