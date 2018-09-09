#!/usr/bin/python
# -*- coding: utf-8 -*-

from pyscipopt import Model, quicksum

def diagonals_top_right_to_bottom_left(board):
    h, w = len(board), len(board[0])
    return [[(h - p + q - 1, q) for q in range(max(p-h+1, 0), min(p+1, w))] for p in range(h + w - 1)]

def diagonals_top_left_to_bottom_right(board):
    h, w = len(board), len(board[0])
    return [[(h - p + q - 1, w - q - 1) for q in range(max(p-h+1, 0), min(p+1, w))] for p in range(h + w - 1)]

def solve_it(w, h):
    model = Model("Queens")

    # First create variables
    board = [[model.addVar(name="board_%s_%s"%(i, j), vtype="BINARY") for j in range(w)] for i in range(h)]

    # Objective
    model.setObjective(quicksum(board[i][j] for j in range(w) for i in range(h)), "maximize")

    # Constraints
    # each row has at most 1 queen
    for i in range(h):
        model.addCons(quicksum(board[i][j] for j in range(w)) <= 1)

    # each column has at most 1 queen
    for j in range(w):
        model.addCons(quicksum(board[i][j] for i in range(h)) <= 1)

    # each diagonal has at most 1 queen
    for diagonals in diagonals_top_right_to_bottom_left(board):
        model.addCons(quicksum(board[i][j] for i, j in diagonals) <= 1)

    # each diagonal, considering other direction, has at most 1 queen
    for diagonals in diagonals_top_left_to_bottom_right(board):
        model.addCons(quicksum(board[i][j] for i, j in diagonals) <= 1)

    # Solve
    model.optimize()

    # prepare the solution in the specified output format
    for i in range(h):
        for j in range(w):
            if model.getVal(board[i][j]) > 0.5:
                print 'Q',
            else:
                print '.',
        print

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 2:
        w = sys.argv[1].strip()
        h = sys.argv[2].strip()
        solve_it(int(w), int(h))
    else:
        print('No board size. Input in order, width and heigth. (i.e. python queens.mip.py 8 8)')
