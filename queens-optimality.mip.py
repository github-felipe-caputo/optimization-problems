#!/usr/bin/python
# -*- coding: utf-8 -*-

from pyscipopt import Model, quicksum

def diagonals_top_right_to_bottom_left(board):
    h, w = len(board), len(board[0])
    return [[(h - p + q - 1, q) for q in range(max(p-h+1, 0), min(p+1, w))] for p in range(h + w - 1)]

def diagonals_top_left_to_bottom_right(board):
    h, w = len(board), len(board[0])
    return [[(h - p + q - 1, w - q - 1) for q in range(max(p-h+1, 0), min(p+1, w))] for p in range(h + w - 1)]

def solve_it(width, height):
    model = Model("Queens")

    # First create variables
    board = [[model.addVar(name="board_%s_%s"%(i, j), vtype="BINARY") for j in range(width)] for i in range(height)]

    # Objective
    model.setObjective(quicksum(board[i][j] for j in range(width) for i in range(height)), "maximize")

    # Constraints
    # each row has at most 1 queen
    for i in range(height):
        model.addCons(quicksum(board[i][j] for j in range(width)) <= 1)

    # each column has at most 1 queen
    for j in range(width):
        model.addCons(quicksum(board[i][j] for i in range(height)) <= 1)

    # each diagonal has at most 1 queen
    for diagonals in diagonals_top_right_to_bottom_left(board):
        model.addCons(quicksum(board[i][j] for i, j in diagonals) <= 1)

    # each diagonal, considering other direction, has at most 1 queen
    for diagonals in diagonals_top_left_to_bottom_right(board):
        model.addCons(quicksum(board[i][j] for i, j in diagonals) <= 1)

    # Solve
    model.optimize()

    # prepare the solution in the specified output format
    for i in range(height):
        for j in range(width):
            if model.getVal(board[i][j]) > 0.5:
                print 'Q',
            else:
                print '.',
        print

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        size = sys.argv[1].strip()
        solve_it(int(size), int(size))
    else:
        print('No board size. Input the size of the board. (i.e. python queens-optimality.mip.py 8)')
