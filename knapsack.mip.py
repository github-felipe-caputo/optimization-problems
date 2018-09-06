#!/usr/bin/python
# -*- coding: utf-8 -*-

from collections import namedtuple
from pyscipopt import Model, quicksum

Item = namedtuple("Item", ['index', 'value', 'weight'])

def solve_it(input_data):
    # parse the input
    lines = input_data.split('\n')

    firstLine = lines[0].split()
    item_count = int(firstLine[0])
    capacity = int(firstLine[1])

    items = []

    for i in range(1, item_count+1):
        line = lines[i]
        parts = line.split()
        items.append(Item(i-1, int(parts[0]), int(parts[1])))

    model = Model("Knapsack")

    # First create variables
    x = {}
    for item in items:
        index = item.index
        x[index] = model.addVar(name="item_(%s)"%(index), vtype="BINARY")

    # Objective
    model.setObjective(quicksum(item.value*x[item.index] for item in items), "maximize")

    # Constraint
    model.addCons(quicksum(item.weight*x[item.index] for item in items) <= capacity)

    # Solve
    model.optimize()

    is_optimal_solution = (model.getStatus() == "optimal")
    objective_val = int(model.getObjVal())

    # prepare the solution in the specified output format
    output_data = str(objective_val) + ' ' + str(1 if is_optimal_solution else 0) + '\n'
    output_data += ' '.join(str(int(model.getVal(x[item.index]))) for item in items)
    return output_data


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:
        print('No input file. Select one. (i.e. python knapsack.mip.py ./data/knapsack/ks_4_0)')
