
class Solver:
    def __init__(self, initial):
        if isinstance(initial, Board):
            self.initial = initial
        else:
            raise Exception('Board class is required')

    def moves(self):
        return self.num_moves

    def solution(self):
        board = self.initial
        pq = MinPQ()
        moves = 0
        while not board.isGoal():
            neighbors = board.neighbors()
            for n in neighbors:
                pq.add(n)
            board = pq.min()
            print board
            moves += 1
        self.num_moves = moves




class MinPQ:
    """minimum priority queue"""


class Board:
    def __init__(self, blocks):
        self.d = self.dimension()
        self.blocks = []
        for i in range(self.d):
            self.blocks.append(map(lambda x: x!='' and x or 0, blocks[i]))

    def __str__(self):
        d = self.d
        fill = len(str(d*d)) - 1
        for i in range(d):
            for c in self.blocks[i]:
                print '% *d' % (fill, c),
            print

    def dimension(self):
        return len(self.blocks)

    def hamming(self):
        """number of blocks out of place"""
        d = self.d
        score = 0
        for i in range(d):
            for j in range(d):
                if not (i == d-1 and j == d-1) and not (self.blocks[i][j] == i*d + j + 1):
                    score += 1
        return score

    def manhattan(self):
        """sum of Manhattan distances between blocks and goal"""
        d = self.d
        score = 0
        for i in range(d):
            for j in range(d):
                if not (i == d-1 and j == d-1) and not (self.blocks[i][j] == i*d + j + 1):
                    v = self.blocks[i][j]
                    goal_i = v / d
                    goal_j = d - v % d
                    score += abs(goal_i - i) + abs(goal_j - j)
        return score

    def isGoal(self):
        d = self.d
        for i in range(d):
            for j in range(d):
                if i == d-1 and j == d-1:
                    return True
                if not self.blocks[i][j] == i*d + j + 1:
                    return False
        return True

    def equal(self, y):
        d = self.d
        for i in range(d):
            for j in range(d):
                if not y[i][j] == self.blocks[i][j]:
                    return False
        return True

    def neighbors(self):
        n = []
        cb = self.blocks
        for i in range(self.d):
            for j in range(self.d):
                if not cb[i][j]:
                    # found the empty one
                    if i-1 >= 0:
                        board = Board(cb)
                        board.blocks[i][j] = cb[i-1][j]
                        board.blocks[i-1][j] = 0
                        n.append(board)
                    if i+1 < self.d:
                        board = Board(cb)
                        board.blocks[i][j] = cb[i+1][j]
                        board.blocks[i+1][j] = 0
                        n.append(board)
                    if j-1 >= 0:
                        board = Board(cb)
                        board.blocks[i][j] = cb[i][j-1]
                        board.blocks[i][j-1] = 0
                        n.append(board)
                    if j+1 < self.d:
                        board = Board(cb)
                        board.blocks[i][j] = cb[i][j+1]
                        board.blocks[i][j+1] = 0
                        n.append(board)
        return n





