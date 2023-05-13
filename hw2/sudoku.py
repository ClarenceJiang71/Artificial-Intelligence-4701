#!/usr/bin/env python
# coding:utf-8

"""
Each sudoku board is represented as a dictionary with string keys and
int values.
e.g. my_board['A1'] = 8
"""
import sys
import time
import statistics

ROW = "ABCDEFGHI"
COL = "123456789"


def print_board(board):
    """Helper function to print board in a square."""
    print("-----------------")
    for i in ROW:
        row = ''
        for j in COL:
            row += (str(board[i + j]) + " ")
        print(row)


def board_to_string(board):
    """Helper function to convert board dictionary to string for writing."""
    ordered_vals = []
    for r in ROW:
        for c in COL:
            ordered_vals.append(str(board[r + c]))
    return ''.join(ordered_vals)


def getCorrelated(var_row, var_column):
    asc = ord(var_row)
    col = int(var_column)
    # Top row, left column
    if asc % 3 == 2 and col % 3 == 1:
        position = [chr(asc + 1) + str(col + 1), chr(asc + 1) + str(col + 2), chr(asc + 2) + str(col + 1),
                    chr(asc + 2) + str(col + 2)]

    # Top row, mid column
    elif asc % 3 == 2 and col % 3 == 2:
        position = [chr(asc + 1) + str(col + 1), chr(asc + 1) + str(col - 1), chr(asc + 2) + str(col + 1),
                    chr(asc + 2) + str(col - 1)]
    # Top row, right column
    elif asc % 3 == 2 and col % 3 == 0:
        position = [chr(asc + 1) + str(col - 1), chr(asc + 1) + str(col - 1), chr(asc + 2) + str(col - 2),
                    chr(asc + 2) + str(col - 2)]
    # Middle row, left column
    elif asc % 3 == 0 and col % 3 == 1:
        position = [chr(asc + 1) + str(col + 1), chr(asc + 1) + str(col + 2), chr(asc - 1) + str(col + 1),
                    chr(asc - 1) + str(col + 2)]
    # Middle row, mid column
    elif asc % 3 == 0 and col % 3 == 2:
        position = [chr(asc + 1) + str(col + 1), chr(asc + 1) + str(col - 1), chr(asc - 1) + str(col + 1),
                    chr(asc - 1) + str(col - 1)]
    # Mid row, right column
    elif asc % 3 == 0 and col % 3 == 0:
        position = [chr(asc + 1) + str(col - 1), chr(asc + 1) + str(col - 2), chr(asc - 1) + str(col - 1),
                    chr(asc - 1) + str(col - 2)]
    # bottom row, left column
    elif asc % 3 == 1 and col % 3 == 1:
        position = [chr(asc - 1) + str(col + 1), chr(asc - 1) + str(col + 2), chr(asc - 2) + str(col + 1),
                    chr(asc - 2) + str(col + 2)]
    # bottom row, mid column
    elif asc % 3 == 1 and col % 3 == 2:
        position = [chr(asc - 1) + str(col + 1), chr(asc - 1) + str(col - 1), chr(asc - 2) + str(col + 1),
                    chr(asc - 2) + str(col - 1)]
    # bottom roow, right column
    else:
        position = [chr(asc - 1) + str(col - 1), chr(asc - 1) + str(col - 2), chr(asc - 2) + str(col - 1),
                    chr(asc - 2) + str(col - 2)]
    return position


def check9grid(var_row, var_column, illegal_list, board):
    position = getCorrelated(var_row, var_column)

    for pos in position:
        if board[pos] != 0 and board[pos] not in illegal_list:
            illegal_list.add(board[pos])
    return illegal_list



def forwardChecking(var_list, collection_list, val, pos):
    for var in var_list:
        t = (var, val)
        if t in collection_list and (var[0] == pos[0] or var[1] == pos[1] or var in getCorrelated(pos[0], pos[1])):
            # [I4, 4]
            return True
    return False


def getMRV(var_list, board):
    max = 10
    final_var = ""
    legal_list = []
    collection_list = set()
    for var in var_list:
        var_row = var[0]
        var_column = var[1]
        illegal_list = set()
        # Take care of all the values that are either on the same row or column
        for key in board:
            if (key[0] == var_row or key[1] == var_column) and board[key] != 0 and board[key] not in illegal_list:
                illegal_list.add(board[key])
        # Deal with the 3x3 grid
        illegal_list = check9grid(var_row, var_column, illegal_list, board)

        total_list = {1, 2, 3, 4, 5, 6, 7, 8, 9}
        remain_list = total_list - illegal_list
        remain_size = len(remain_list)

        if remain_size < max:
            max = remain_size
            final_var = var
            legal_list = remain_list

        # merge the variable name with the remain list set to form a tuple which is added into a set for
        # forward checking
        t = (var, ) + tuple(remain_list)
        collection_list.add(t)
    return final_var, legal_list, collection_list


def backtracking(board):
    """Takes a board and returns solved board."""
    # TODO: implement this
    solved_board = backtrackRecursion(board)
    return solved_board


def backtrackRecursion(board):
    if 0 not in board.values():
        return board
    var_list = [key for key in board if board[key] == 0]
    pos, legal_list, collection_list = getMRV(var_list, board)
    for val in legal_list:
        board[pos] = val
        # forward checking, need the rest of the variable that is not current position
        unassigned_list = [value for value in var_list if value != pos]
        collection_list = getMRV(unassigned_list, board)[2]
        if forwardChecking(unassigned_list, collection_list, val, pos):
            continue
        result = backtrackRecursion(board)
        if result is not False:
            return result
        else:
            board[pos] = 0
    return False


def checkAnswer():
    f1 = open("sudokus_finish.txt", "r")
    f2 = open("output.txt", "r")

    i = 0

    for line1 in f1:
        i += 1

        for line2 in f2:

            # matching line1 from both files
            if line1 == line2:
                # print IDENTICAL if similar
                print("Line ", i, ": IDENTICAL")
            else:
                print("Line ", i, ":")
                # else print that line from both files
                print("\tFile 1:", line1, end='')
                print("\tFile 2:", line2, end='')
            break

    # closing files
    f1.close()
    f2.close()


if __name__ == '__main__':
    # Test parameter: 003020600900305001001806400008102900700000008006708200002609500800203009005010300
    # First error: 000100702030950000001002003590000301020000070703000098800200100000085060605009000
    if len(sys.argv) > 1:

        # Running sudoku solver with one board $python3 sudoku.py <input_string>.
        print("The problem is: " + sys.argv[1])

        # Parse boards to dict representation, scanning board L to R, Up to Down
        board = {ROW[r] + COL[c]: int(sys.argv[1][9 * r + c])
                 for r in range(9) for c in range(9)}
        solved_board = backtracking(board)
        print("The solved board is: ")
        print_board(solved_board)

        # Write board to file
        out_filename = 'output.txt'
        outfile = open(out_filename, "w")
        outfile.write(board_to_string(solved_board))
        outfile.write('\n')

    else:

        # Running sudoku solver for boards in sudokus_start.txt $python3 sudoku.py

        #  Read boards from source.
        src_filename = 'sudokus_start.txt'
        try:
            srcfile = open(src_filename, "r")
            sudoku_list = srcfile.read()
        except:
            print("Error reading the sudoku file %s" % src_filename)
            exit()

        # Setup output file
        out_filename = 'output.txt'
        outfile = open(out_filename, "w")

        # Solve each board using backtracking
        count = 0
        time_list = []
        for line in sudoku_list.split("\n"):
            if len(line) < 9:
                continue
            # Parse boards to dict representation, scanning board L to R, Up to Down
            board = {ROW[r] + COL[c]: int(line[9 * r + c])
                     for r in range(9) for c in range(9)}

            # Print starting board. TODO: Comment this out when timing runs.
            # print_board(board)

            # Print solved board. TODO: Comment this out when timing runs.
            # print_board(solved_board)

            # Solve with backtracking
            startTime = time.time()
            solved_board = backtracking(board)
            endTime = time.time()
            time_list.append(endTime-startTime)

            if solved_board:
                count+=1

            # Write board to file
            outfile.write(board_to_string(solved_board))
            outfile.write('\n')

        # checkAnswer()
        # print(f"Total sudokus solved: {count}")
        # print(f"Min time is {min(time_list)}")
        # print(f"Max time is {max(time_list)}")
        # print(f"Average time is {sum(time_list) / len(time_list)}")
        # print(f"Standard deviation time is {statistics.pstdev(time_list)}")
        # print("Finishing all boards in file.")
