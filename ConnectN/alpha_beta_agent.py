import math
import agent
import copy
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
        best_move = -1
        best_move_val = -1000000000 #just dumb negative make it in a better way
        free_cols = brd.free_cols()
        for col in free_cols:
            new_board = brd.copy()
            # Add a token to the new board
            # (This internally changes nb.player, check the method definition!)
            new_board.add_token(col)
            value = self.maximize(new_board, 0)
            if(value > best_move_val):
                best_move = col
                best_move_val = value

        return best_move


    def minimize(self, brd, depth):
        value = 10000000 # just dumb high make it in a better way
        if(depth == self.max_depth):
            return self.score_board(brd)

        successors = self.get_successors(brd)
        for new_board in successors:
            value = min(value, self.maximize(new_board[0], depth+1))
        return value

    def maximize(self, brd, depth):
        value = -10000000  # just dumb negative make it in a better way
        if(depth == self.max_depth):
            return self.score_board(brd)

        for new_board in self.get_successors(brd):
            value = max(value, self.minimize(new_board[0], depth+1))
        return value

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


    def create_rings(self, brd):
        """
        Creates a list of rings which are represented as 4 corners. These rings start at the middle of the board
        and pulsate out.
        :param brd: the game board to base everything
        :return: a list of rings
        """
        center_h = (brd.h // 2)
        center_w = (brd.w // 2)
        rings = []
        range = 1
        one_valid = True
        while one_valid:
            corners = []
            if center_h - range < 0 and center_w - range < 0 and center_h + range >= brd.h and center_w + range >= brd.w:
                one_valid = False
                break

            TL = (center_h - range, center_w - range)
            TR = (center_h - range, center_w + range)
            BL = (center_h + range, center_w - range)
            BR = (center_h + range, center_w + range)

            corners.append(copy.deepcopy(TL))
            corners.append(copy.deepcopy(TR))
            corners.append(copy.deepcopy(BL))
            corners.append(copy.deepcopy(BR))
            rings.append(copy.deepcopy(corners))
            range += 1
        return rings

    def get_ring_value(self, brd, h, w, rings):
        """
        Gets the value of the cell (h,w)  with its relation to ring location. The farther out from the middle cell
        it is, the lower the value
        :param brd: the game board grid
        :param h: height value of the cell
        :param w: width value of the cell
        :param rings: a list of rings
        :return:
        """
        center_h = (brd.h // 2)
        center_w = (brd.w // 2)
        max_points = ((brd.h + brd.w) // 2)
        range = 1
        if h == center_h and w == center_w:
            return max_points + 1
        else:
            for ring in rings:
                TL = ring[0]
                TR = ring[1]
                BL = ring[2]
                BR = ring[3]

                #Top of ring
                if h == TL[0] and TL[1] <= w and TR[1] >= w:
                    return max_points - int(range*1.5)
                #Bottom of ring
                if h == BL[0] and BL[1] <= w and BR[1] >= w:
                    return max_points - int(range*1.5)
                #Left of ring
                if w == TL[1] and TL[0] <= h and BL[0] >= h:
                    return max_points - int(range*1.5)
                #Right of ring
                if w == TR[1] and TR[0] <= h and BR[0] >= h:
                    return max_points - int(range*1.5)
                range += 1
        return None

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
    print(abs.create_rings(board))
    print(abs.get_ring_value(board,2,3,abs.create_rings(board)))
