matrix = []

def parse():
    row_length = len(matrix)
    col_length = len(matrix[0])

    history = [0] * col_length
    for rowIndex in range(row_length):
        connected = [0] * col_length
        for colIndex, cell in enumerate(matrix[rowIndex]):
            if is_connected_until(rowIndex, colIndex, history):
                connected[colIndex] = 1
        history = connected
    print connected
    return [index for index, v in enumerate(connected) if v == 1]

def is_connected_until(rowIndex, colIndex, history):
    if rowIndex == 0:
        return matrix[rowIndex][colIndex] == '1'
    if colIndex == 0:
        return matrix[rowIndex][colIndex] == '1' and (history[colIndex] or history[colIndex+1])
    return matrix[rowIndex][colIndex] == '1' and \
           (history[colIndex-1] or history[colIndex] or history[colIndex+1])


def show(board):
    board = board.split('\n')
    global matrix
    for row in board:
        a_row = []
        for p in row:
            print p,
            if p == '1' or p == '.' :
                a_row.append(p)
        print
        if a_row:
            matrix.append(a_row)





board = """

1......1
.1......
..1.....
...1....
........
...1.1..
..1..1..
11....1.

"""

show(board)
print parse()