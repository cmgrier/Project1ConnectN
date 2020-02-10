import math
import agent
import copy
import board
import time

###########################
# Alpha-Beta Search Agent #
###########################

class AlphaBetaAgent(agent.Agent):
    """Agent that uses alpha-beta search"""
    big_negative = -10000000
    big_positive = 100000000
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
        best_move = -1
        best_move_val = self.big_negative
        alpha = self.big_negative
        beta = self.big_positive
        free_cols = brd.free_cols()
        if self.player == 1:
            opp = 2
        else:
            opp = 1
        for col in free_cols:
            new_board = brd.copy()
            # Add a token to the new board
            # (This internally changes nb.player, check the method definition!)
            new_board.add_token(col)
            outcome = new_board.get_outcome()
            possible_loss = self.one_play_away(new_board, opp)
            if outcome == 0:
                value = self.maximize(new_board, 0, alpha, beta)
            elif outcome != self.player:
                value = -9999
            else:
                value = 9999
            if possible_loss != -1:
                value = -99999
            if value > best_move_val:
                best_move = col
                best_move_val = value

        return best_move

    #
    #The minimize half of minimax.
    # PARAM [board.Board] brd: the game board for the state
    # PARAM [int] depth: the current iteration
    # PARAM [int] alpha: the alpha minimum for alpha beta pruning
    # PARAM [int] beta: the beta maximum for alpha beta pruning
    # RETURN [float]: the minimal value for the nodes leaf nodes
    #
    def minimize(self, brd, depth, alpha, beta):
        value = self.big_positive
        if depth == self.max_depth:
            return self.score_board(brd, depth)

        successors = self.get_successors(brd)
        for new_board in successors:
            outcome = new_board[0].get_outcome()
            if outcome == 0:
                value = min(value, self.maximize(new_board[0], depth + 1, alpha, beta))
            elif outcome != self.player:
                value = -999
            else:
                value = 999
            if value <= alpha:
                return value
            beta = min(beta, value)
        return value

        #
        # The maximize half of minimax.
        # PARAM [board.Board] brd: the game board for the state
        # PARAM [int] depth: the current iteration
        # PARAM [int] alpha: the alpha minimum for alpha beta pruning
        # PARAM [int] beta: the beta maximum for alpha beta pruning
        # RETURN [float]: the maximum value for the nodes leaf nodes
        #
    def maximize(self, brd, depth, alpha, beta):
        value = self.big_negative
        if depth == self.max_depth:
            return self.score_board(brd, depth)

        for new_board in self.get_successors(brd):
            outcome = new_board[0].get_outcome()
            if outcome == 0:
                value = max(value, self.minimize(new_board[0], depth + 1, alpha, beta))
            elif outcome != self.player:
                value = -999
            else:
                value = 999
            if value >= beta:
                return value
            alpha = max(alpha, value)
        return value

    #Gives a score to a supplied board state
    #
    #PARAM [board.Board] brd: the board state to evaluate
    #RETURN [int]: the score of the board

    def score_board(self, brd, depth):
        """Scores the given board according to benchmarks"""
        if brd.get_outcome() == self.player:
            return self.big_positive
        if brd.get_outcome() == 0:
            score = 0
            if self.player == 1:
                opp = 2
            else:
                opp = 1
            if self.one_play_away(brd, self.player) != -1:
                score += 1000
            elif self.one_play_away(brd, opp) != -1:
                score -= 1000
            if depth < 6: # this is to help speed of agent in higher depths
                rings = self.create_rings(brd)
                for r in range(0, brd.h):
                    for c in range(0, brd.w):
                        score += self.get_ring_value(brd, r, c, rings)
                        score += self.evaluate_token(brd, r, c)
                        score += self.two_move_setup(brd, r, c, self.player) * 100
            return score
        else:
            return self.big_negative

    def one_play_away(self, brd, player):
        """Returns column if player can put a token there and win, -1 otherwise"""
        if brd.get_outcome() != 0:
            return -1
        free_slots = brd.free_cols()
        for col in free_slots:
            copy = brd.copy()
            copy.player = player
            copy.add_token(col)
            if copy.get_outcome() != 0:
                return col
        return -1

    # this function may be able to be removed, disregard for now. Also it doesn't cover all 2 move setups
    def two_move_setup(self, brd, r, c, player):
        """returns 1 if player has n-2 tokens connecting and two empty places on either side"""
        token = brd.board[r][c]
        if token == 0:
            return 0
        possible_setup_dir = []
        two_move_setups = 0
        for pdir in range(1, 4):
            if self.look_for_continuous_line_in_dir(brd, r, c, pdir) == brd.n - 2:
                possible_setup_dir.append(pdir)

        for dir in possible_setup_dir:
            left = [r, c]
            right = [r, c]
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
            if self.valid_coordinate(brd, left[0] - ir, left[1] - ic):
                while brd.board[left[0] - ir][left[1] - ic] == token:
                    left = [left[0] - ir, left[1] - ic]
                    if not self.valid_coordinate(brd, left[0] - ir, left[1] - ic):
                        break
            if self.valid_coordinate(brd, right[0] + ir, right[1] + ic):
                while brd.board[right[0] + ir][right[1] + ic] == token:
                    right = [right[0] + ir, right[1] + ic]
                    if not self.valid_coordinate(brd, right[0] + ir, right[1] + ic):
                        break

            end1 = [left[0] - ir, left[1] - ic]
            end2 = [right[0] + ir, right[1] + ic]

            if self.is_spot_open_for_placement(brd, end1[0], end1[1]) and self.is_spot_open_for_placement(brd, end2[0], end2[1]):
                two_move_setups += 1
        if token != player:
            return two_move_setups * -2
        return two_move_setups


    def is_spot_open_for_placement(self, brd, r, c):
        """returns true if given location is available for token next turn"""
        if not self.valid_coordinate(brd, r, c):
            return False
        token = brd.board[r][c]
        if token != 0:
            return False
        elif r == 0:
            return True
        elif self.valid_coordinate(brd, r - 1, c):
            return brd.board[r - 1][c] != 0


    def look_for_continuous_line_in_dir(self, brd, r, c, dir):
        """returns number of tokens in a row extending from given direction"""
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
        token = brd.board[r][c]
        rn = r + ir
        cn = c + ic
        in_a_row = 1
        if self.valid_coordinate(brd, rn, cn):
            while brd.board[rn][cn] == token:
                in_a_row += 1
                rn += ir
                cn += ic
                if not self.valid_coordinate(brd, rn, cn):
                    break

        rn = r - ir
        cn = c - ic
        if self.valid_coordinate(brd, rn, cn):
            while brd.board[rn][cn] == token:
                in_a_row += 1
                rn -= ir
                cn -= ic
                if not self.valid_coordinate(brd, rn, cn):
                    break
        return in_a_row

    def valid_coordinate(self, brd, r, c):
        """Checks if given coordinates are valid for the board"""
        if r >= brd.h:
            return False
        elif r < 0:
            return False
        elif 0 > c:
            return False
        elif c >= brd.w:
            return False
        return True

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

        return in_p_dir + in_n_dir + .1 * (n_open + p_open)

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

if __name__ == '__main__':
    data = [[0, 0, 2, 2, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0]]
    board = board.Board(data, 7, 6, 4)
    aba = AlphaBetaAgent("abba", 4)
    aba.player = 1
    start = time.time()
    play = aba.go(board)
    end = time.time()
    print("P1 puts token: " + str(play))
    print("Time elapsed: " + str(end - start))

    backup = [[0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0]]
