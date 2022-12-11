import numpy as np
# from pyscript import *
# from utils import add_class, remove_class

# tasks = []

# # define the task template that will be use to render new templates to the page
# task_template = Element("task-template").select(".task", from_content=True)
# task_list = Element("list-tasks-container")
# new_task_content = Element("new-task-content")


height = 4
width = 4
iterations = 0
is_solved = 0

left = 0
right = 1
down = 2
up = 3

row_start = 0
col_start = 0
row_end = 0
col_end = 0
target = 0

previous_row_start = 0
previous_col_start = 0
previous_row_end = 3
previous_col_end = 3

row_pos = row_start
col_pos = col_start

path = np.zeros((height, width), dtype=int)
grid = np.zeros((height, width), dtype=int)


# Display the grid in the terminal
def display_grid(matrix, is_path):
    data = ""
    for row in range(height):
        for column in range(width):
            if column == col_start and row == row_start and is_path:
                data += f' {int(matrix[row][column])}*\t'
            elif column == col_end and row == row_end and is_path:
                data += f' {int(matrix[row][column])}!\t'
            else:
                data += f' {int(matrix[row][column])}\t'  # Do not display the start and the end characters
        data += '\n\r'
    return data


# Check if the square is unoccupied by another part of the path
def is_empty(row, col):
    if path[row][col]:
        return False
    else:
        return True


# Check if the square is inside the grid
def is_inside(row, col):
    if row < 0 or row >= height:
        return False
    if col < 0 or col >= width:
        return False
    return True


# Handling of the next move direction
def move(board, direction):
    global row_pos
    global col_pos
    row = board[0]
    col = board[1]
    row_des = row
    col_des = col

    if direction == left:
        col_des = col - 1
    elif direction == right:
        col_des = col + 1
    elif direction == down:
        row_des = row + 1
    elif direction == up:
        row_des = row - 1

    if is_inside(row_des, col_des):
        if is_empty(row_des, col_des):
            row_pos = row_des
            col_pos = col_des
            return True  # A surrounding box is available
    return False  # No surrounding box is available


def solve_board(board):
    global grid
    global path
    global target
    global row_pos
    global col_pos
    global iterations
    global is_solved

    row = board[0]
    col = board[1]
    total = board[2]
    step = board[3]

    step = step + 1
    path[row][col] = step
    total = total + grid[row][col]
    board = [row, col, total, step]
    if total == target and row == row_end and col == col_end:
        is_solved = 1
        return True

    for i in range(0, 4):
        iterations = iterations + 1
        if move(board, i):
            new_board = [row_pos, col_pos, total, step]
            if solve_board(new_board):
                return True
    path[row][col] = 0
    return False  # No more move remaining


def solve(pathData):
    global grid
    global path
    global target
    global row_pos
    global col_pos
    global row_start
    global col_start
    global row_end
    global col_end
    global iterations
    global is_solved

    row_start = pathData[0]
    col_start = pathData[1]
    row_end = pathData[2]
    col_end = pathData[3]
    target = pathData[4]
    grid = pathData[5]

    row_pos = row_start
    col_pos = col_start

    path = np.zeros((height, width), dtype=int)
    board = [row_start, col_start, 0, 0]

    iterations = 0
    is_solved = 0

    pyscript.write('solveStatus', 'Solving...')

    if solve_board(board):
        pyscript.write('solveStatus', f'The board is solved! {iterations} iterations were needed.')
        pyscript.write('finalGrid', f'The path is:\r\n {display_grid(path, False)}')
        pyscript.write('o1', int(path[0][0]))
        pyscript.write('o2', int(path[0][1]))
        pyscript.write('o3', int(path[0][2]))
        pyscript.write('o4', int(path[0][3]))
        pyscript.write('o5', int(path[1][0]))
        pyscript.write('o6', int(path[1][1]))
        pyscript.write('o7', int(path[1][2]))
        pyscript.write('o8', int(path[1][3]))
        pyscript.write('o9', int(path[2][0]))
        pyscript.write('o10', int(path[2][1]))
        pyscript.write('o11', int(path[2][2]))
        pyscript.write('o12', int(path[2][3]))
        pyscript.write('o13', int(path[3][0]))
        pyscript.write('o14', int(path[3][1]))
        pyscript.write('o15', int(path[3][2]))
        pyscript.write('o16', int(path[3][3]))
    else:
        pyscript.write('solveStatus', 'The board could not be solved :(')


def getData():
    global height
    global width
    global grid
    global path
    global iterations
    global is_solved

    table = np.zeros((height, width), dtype=int)

    for row in range(height):
        for column in range(width):
            table[row][column] = Element(f'i{4*row+column+1}').element.value
    
    pyscript.write('solveStatus', 'Getting the parameters')
    rowStart = int(Element('startRow').element.value)
    colStart = int(Element('startCol').element.value)
    rowEnd = 3  # int(Element('endRow').element.value)
    colEnd = 3  # int(Element('endCol').element.value)
    targetValue = int(Element('targetSum').element.value)

    pathData = [rowStart, colStart, rowEnd, colEnd, targetValue, table]
    return pathData


def handle_click(e):
    pathStartData = getData()
    pyscript.write('solveStatus', 'Data acquired!')
    solve(pathStartData)
