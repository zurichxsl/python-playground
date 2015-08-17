import math

dir = '/Users/sxu/Downloads/8puzzle/'
import Queue


def memoize(function):
    memo = {}

    def wrapper(*args):
        if args in memo:
            return memo[args]
        else:
            rv = function(*args)
            memo[args] = rv
            return rv

    return wrapper


class Board:
    def __init__(self, blocks, board=None):
        self.blocks = blocks

        if board:
            self.d = board.d
            self.moves = board.moves + 1
            self.parent = board
        else:
            self.d = self.dimension()
            self.moves = 0
            self.parent = None
        # h = self.hamming()
        m = self.manhattan()
        self.isGoal = m == 0
        self.score = self.moves + m

    def __str__(self):
        d = self.d
        keys = ''
        for i in range(d * d):
            if i > 0:
                if i % d == 0:
                    keys += '\n'
                else:
                    keys += ' '
            keys += '%2d' % self.blocks[i]
        return keys

    def show(self):
        print str(self)
        print 'moves %d, score %d' % (self.moves, self.hamming())
        print

    def dimension(self):
        return int(math.sqrt(len(self.blocks)))

    def index(self, i, j):
        return i * self.d + j

    def index_to_ij(self, index):
        return index / self.d, index % self.d

    def __setitem__(self, key, value):
        self.blocks[self.index(key[0], key[1])] = value

    def __getitem__(self, item):
        # if type(item) is tuple:
        return self.blocks[self.index(item[0], item[1])]

    # @memoize
    def hamming(self):
        """number of blocks out of place"""
        n = self.d * self.d
        score = 0
        for i in range(n):
            if i == n - 1:
                if self.blocks[i] != 0:
                    score += 1
            elif self.blocks[i] != i + 1:
                score += 1
        return score

    def manhattan(self):
        """sum of Manhattan distances between blocks and goal"""
        d = self.d
        score = 0
        for x in range(d * d):
            if self.blocks[x] != 0 and self.blocks[x] != x + 1:
                goal_i, goal_j = self.index_to_ij(self.blocks[x] - 1)
                i, j = self.index_to_ij(x)
                score += abs(goal_i - i) + abs(goal_j - j)
        return score

    # def isGoal(self):
    #     return self.hamming() == 0

    # def equal(self, y):
    #     d = self.d
    #     for i in range(d):
    #         for j in range(d):
    #             if not y[i][j] == self.blocks[i][j]:
    #                 return False
    #     return True

    def newtuple(self, x0, y0, x1, y1):
        l = list(self.blocks)
        l[self.index(x0, y0)] = self[x1, y1]
        l[self.index(x1, y1)] = self[x0, y0]
        return tuple(l)

    def neighbors(self):
        idxzero = self.blocks.index(0)
        i, j = self.index_to_ij(idxzero)
        n = []
        if i - 1 >= 0:
            n.append(self.newtuple(i, j, i - 1, j))
        if i + 1 < self.d:
            n.append(self.newtuple(i, j, i + 1, j))
        if j - 1 >= 0:
            n.append(self.newtuple(i, j, i, j - 1))
        if j + 1 < self.d:
            n.append(self.newtuple(i, j, i, j + 1))
        return n


class MinPQ:
    """minimum priority queue, parent's key no bigger than children's keys"""

    def __init__(self, initial):
        """array representation, indice starts at 1, take nodes in level order"""
        self.array = initial or []
        self.length = 0

    def show(self):
        pq_score = []
        for i in xrange(1, self.size()):
            pq_score.append((i, self.array[i].score))
        print pq_score

    def insert(self, v):
        """insert v into min priority queue"""
        if not self.size():
            self.array.append('')
        self.array.append(v)
        k = self.size() - 1
        inserted_index = self.swim(k)
        return inserted_index

    def size(self):
        return len(self.array)

    def delMin(self):
        min = self.array[1]
        last = self.array[self.size() - 1]
        self.array[1] = last
        self.array = self.array[:-1]
        self.sink(1)
        if self.size() == 1:
            self.array.pop()
        return min

    def sink(self, k):
        """when a parent's key becomes bigger than its children's key, sink down"""
        while 2 * k < self.size():
            j = 2 * k
            if j + 1 < self.size() and self.array[j + 1].score < self.array[j].score:
                # choose the smaller one
                j += 1
            if self.array[k].score < self.array[j].score:
                break
            temp = self.array[j]
            self.array[j] = self.array[k]
            self.array[k] = temp
            k = j
        return k

    def swim(self, k):
        """when child's key becomes smaller than its parent's key, swim up"""
        while k > 1 and self.array[k].score < self.array[k / 2].score:
            temp = self.array[k]
            self.array[k] = self.array[k / 2]
            self.array[k / 2] = temp
            k /= 2
        return k


class Solver:
    def __init__(self, initial):
        self.visited_nodes = 0
        if isinstance(initial, Board):
            self.initial = initial
        else:
            raise Exception('Board class is required')

    def solution(self):
        tries = 0
        board = self.initial
        pq = Queue.PriorityQueue()
        visited = set()
        visited.add(board.blocks)
        while not board.isGoal:
            if tries < 10:
                print board
                print ''
            tries += 1
            neighbors = board.neighbors()
            for n in neighbors:
                if n not in visited:
                    newboard = Board(n, board)
                    pq.put((newboard.score, newboard))
                    visited.add(n)
            score, board = pq.get()
        print " - Found solution after " + str(tries) + " tries!"
        return board


def test_solver(blocks):
    initial = Board(tuple(blocks))
    # solver = Solver(initial)
    # for b in solver.solution('manhattan'):
    #     b
    # print '=====================manhattan====%s===================' % solver.moves()
    import time
    start = time.time()
    b = Solver(initial).solution()
    if b:
        print '=====================hamming====%s==========in %s=========' % (b.moves, time.time() - start)
        # while b:
        #     print str(b)
        #     print ''
        #     b = b.parent
        # b.show()


def main(dir, fname):
    lines = [line.rstrip('\n').strip() for line in open(dir + fname) if line.rstrip('\n')]
    blocks = []
    size = 0
    for index, line in enumerate(lines):
        if index == 0:
            size = int(line)
        elif line and (index <= size):
            for v in line.split():
                blocks.append(int(v))
    print fname
    test_solver(blocks)
    print


def test():
    initial = Board([0, 1, 3, 4, 2, 5, 7, 8, 6])
    solver = Solver(initial)
    for b in solver.solution('hamming'):
        b.show()
        print


if __name__ == '__main__':
    # import os
    # for i in os.listdir(dir):
    #     if i.find('unsolvable') > 0:
    #         continue
    #     else:
    #         main(dir, i)

    # p = MinPQ([89, 79, 46, 69, 59, 25, 44, 60, 30, 20 ])

    main(dir, 'puzzle32.txt')
    # test_solver([
    #     [3,1,6,4],[5,0,9,7], [10,2,11,8], [13,15,14,12]
    # ])