class Board:
    def __init__(self, blocks):
        self.blocks = []
        for i in range(len(blocks)):
            self.blocks.append([j for j in blocks[i]])
        self.d = self.dimension()

    def __str__(self):
        d = self.d
        keys = []
        for i in range(d):
            keys.append(' '.join([str(c) for c in self.blocks[i]]))
        return ','.join(keys)

    def show(self):
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
        return n


class MinPQ:
    """minimum priority queue, parent's key no bigger than children's keys"""
    def __init__(self):
        """array representation, indice starts at 1, take nodes in level order"""
        self.array = []
        self.length = 0

    def insert(self, v, fn):
        """insert v into min priority queue"""
        if not self.size():
            self.array.append('')
        self.array.append(v)
        k = self.size() - 1
        self.swim(k, fn)

    def size(self):
        return len(self.array)

    def delMin(self, fn):
        min = self.array[1]
        last = self.array[self.size()-1]
        self.array[1] = last
        self.array = self.array[:-1]
        self.sink(1, fn)
        if self.size() == 1:
            self.array.pop()
        return min

    def sink(self, k, fn):
        """when a parent's key becomes bigger than its children's key, sink down"""
        while 2*k < self.size():
            j = 2*k
            if j+1 < self.size() and getattr(self.array[j+1], fn)() < getattr(self.array[j], fn)():  # choose the smaller one
                j += 1
            if getattr(self.array[k], fn)() < getattr(self.array[j], fn)():
                break
            temp = self.array[j]
            self.array[j] = self.array[k]
            self.array[k] = temp
            k *= 2

    def swim(self, k, fn):
        """when child's key becomes smaller than its parent's key, swim up"""
        #while k > 1 and getattr(self.array[k], fn)() < getattr(self.array[k/2], fn)():
        while k > 1 and getattr(self.array[k], fn)() < getattr(self.array[k/2], fn)():
            temp = self.array[k]
            self.array[k] = self.array[k/2]
            self.array[k/2] = temp
            k /= 2



class Solver:
    def __init__(self, initial):
        self.num_moves = 0
        if isinstance(initial, Board):
            self.initial = initial
        else:
            raise Exception('Board class is required')

    def moves(self):
        return self.num_moves

    def solution(self, fn):
        board = self.initial
        pq = MinPQ()
        visited = {}
        visited[str(board)] = 1

        while not board.isGoal():
            neighbors = board.neighbors()
            for n in neighbors:
                if str(n) not in visited:
                    pq.insert(n, fn)
                    visited[str(n)] = 1
            board = pq.delMin(fn)
            self.num_moves += 1
            yield board







def test():
    pq = MinPQ()
    pq.insert({'v': 10}, 'v')
    pq.insert({'v': 4}, 'v')
    pq.insert({'v': 5}, 'v')
    pq.insert({'v': 18}, 'v')
    pq.insert({'v': 3}, 'v')

    print pq.array
    print pq.delMin('v')
    print pq.array
    print pq.delMin('v')
    print pq.array
    print pq.delMin('v')
    print pq.array
    print pq.delMin('v')
    print pq.array
    print pq.delMin('v')
    print pq.array



initial = Board([
    [0,1,3],[4,2,5],[7,8,6]
    ])
solver = Solver(initial)
for b in solver.solution('manhattan'):
    b.show()
    print


print '============================================'
solver = Solver(initial)
for b in solver.solution('hamming'):
    b.show()
    print