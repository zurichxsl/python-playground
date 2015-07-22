dir = '/Users/sxu/Downloads/8puzzle/'
import Queue

class Board:
    def __init__(self, blocks):
        self.blocks = []
        for i in range(len(blocks)):
            self.blocks.append([j for j in blocks[i]])
        self.d = self.dimension()
        self.moves = 0
        self.score = 0

    def __str__(self):
        d = self.d
        keys = []
        for i in range(d):
            keys.append(' '.join([str(c) for c in self.blocks[i]]))
        return ','.join(keys)

    def show(self):
        d = self.d
        total = len(str(d*d)) + 1
        for i in range(d):
            for c in self.blocks[i]:
                print '% *d' % (total, c),
            print
        print 'moves %d, score %d' % (self.moves, self.hamming())
        print

    def dimension(self):
        return len(self.blocks)

    def hamming(self):
        """number of blocks out of place"""
        d = self.d
        score = 0
        for i in range(d):
            for j in range(d):
                if i == d-1 and j == d-1:
                    if self.blocks[i][j] != 0:
                        score +=1
                elif not (self.blocks[i][j] == i*d + j + 1):
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
                        board.moves = self.moves + 1
                        board.score = board.hamming() + board.moves
                        n.append(board)
                    if i+1 < self.d:
                        board = Board(cb)
                        board.blocks[i][j] = cb[i+1][j]
                        board.blocks[i+1][j] = 0
                        board.moves = self.moves + 1
                        board.score = board.hamming() + board.moves
                        n.append(board)
                    if j-1 >= 0:
                        board = Board(cb)
                        board.blocks[i][j] = cb[i][j-1]
                        board.blocks[i][j-1] = 0
                        board.moves = self.moves + 1
                        board.score = board.hamming() + board.moves
                        n.append(board)
                    if j+1 < self.d:
                        board = Board(cb)
                        board.blocks[i][j] = cb[i][j+1]
                        board.blocks[i][j+1] = 0
                        board.moves = self.moves + 1
                        board.score = board.hamming() + board.moves
                        n.append(board)
                    return n
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
        last = self.array[self.size()-1]
        self.array[1] = last
        self.array = self.array[:-1]
        self.sink(1)
        if self.size() == 1:
            self.array.pop()
        return min

    def sink(self, k):
        """when a parent's key becomes bigger than its children's key, sink down"""
        while 2*k < self.size():
            j = 2*k
            if j+1 < self.size() and self.array[j+1].score < self.array[j].score:
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
        while k > 1 and self.array[k].score < self.array[k/2].score:
            temp = self.array[k]
            self.array[k] = self.array[k/2]
            self.array[k/2] = temp
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
        board = self.initial
        pq = Queue.PriorityQueue()
        visited = set()
        visited.add(str(board))

        while not board.isGoal():
            neighbors = board.neighbors()
            for n in neighbors:
                if str(n) not in visited:
                    pq.put((n.score, n))
                    visited.add(str(n))
            score, board = pq.get()
        return board


def test_solver(blocks):
    initial = Board(blocks)
    # solver = Solver(initial)
    # for b in solver.solution('manhattan'):
    #     b
    # print '=====================manhattan====%s===================' % solver.moves()
    import time
    start = time.time()
    b = Solver(initial).solution()
    if b:
        print '=====================hamming====%s==========in %s=========' % (b.moves, time.time() - start)
        #b.show()


def main(dir, fname):
    lines = [line.rstrip('\n').strip() for line in open(dir+fname) if line.rstrip('\n')]
    blocks = []
    size = 0
    for index, line in enumerate(lines):
        if index == 0:
            size = int(line)
        elif line and (index <= size):
            blocks.append([int(v) for v in line.split()])
    print fname
    test_solver(blocks)
    print


def test():
    initial = Board([
        [0,1,3],
        [4,2,5],
        [7,8,6]
    ])
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

    #p = MinPQ([89, 79, 46, 69, 59, 25, 44, 60, 30, 20 ])

    #main(dir, 'puzzle32.txt')
    # test_solver([
    #     [3,1,6,4],[5,0,9,7], [10,2,11,8], [13,15,14,12]
    # ])



