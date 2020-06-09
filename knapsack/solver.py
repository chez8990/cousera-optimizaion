#!/usr/bin/python
# -*- coding: utf-8 -*-

import numpy as np

from collections import namedtuple
Item = namedtuple("Item", ['index', 'value', 'weight'])

def read_data(input_data):


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

    return items, item_count, capacity


def bnb(input_data):
    items, item_count, capacity = read_data(input_data)

    max_value = 0
    max_value_sum = sum([item.value for item in items])

    max_val = 0
    record = []
    current_taken = []
    current_val = 0
    current_weight = 0
    estimate = max_value_sum

    q = [(0, current_val, current_weight, estimate, current_taken)]
    # print(items, capacity)
    while q:
        print(q)
        index, current_val, current_weight, estimate, current_taken = q.pop()
        if index >= item_count:
            continue

        item = items[index]
        # check if the item is heavier than available weight
        if item.weight + current_weight > capacity:
            continue

        # max_val = max(max_val, current_val + item.value)

        if item.value + current_val > max_val:
            max_val = item.value + current_val
            record = current_taken + [index]

        # take the item
        q.append((index + 1, current_val + item.value, current_weight + item.weight, estimate, current_taken + [index]))

        # don't take the item
        # check if it exceeds the lower bound
        if estimate - item.value < max_value:
            continue
        else:
            q.append((index + 1, current_val, current_weight, estimate-item.value, current_taken))

    # taken = [0 for _ in range(item_count)]

    taken = [0 for _ in range(item_count)]
    for i in record:
        taken[i] = 1
    return max_val, taken

def dp(input_data):
    items, item_count, capacity = read_data(input_data)
    DP = np.zeros((2, capacity + 1), dtype=np.int32)
    taken = [[[] for _ in range(capacity+1)] for _ in range(2)]

    for i in range(1, item_count+1):
        item = items[i - 1]
        for k in range(1, capacity+1):
            if item.weight <= k:
                if DP[0, k - item.weight] + item.value > DP[0, k]:
                    DP[1, k] = DP[0, k - item.weight] + item.value
                    temp_taken = taken[0][k-item.weight].copy()
                    temp_taken.append(i-1)
                    taken[1][k] = temp_taken
                else:
                    DP[1, k] = DP[0, k]
                    taken[1][k] = taken[0][k]
            else:
                DP[1, k] = DP[0, k]
                taken[1][k] = taken[0][k]
        DP[0] = DP[1].copy()
        taken[0] = taken[1].copy()


    value = DP[1, capacity]
    record = taken[1][capacity]
    taken = [0 for _ in range(item_count)]
    for i in record:
        taken[i] = 1

    return value, taken

def solve_it(input_data):
    items, item_count, capacity = read_data(input_data)
    print(item_count, capacity)
    if capacity >= 100000:
        # pass
        value, taken = bnb(input_data)
    else:
        value, taken = dp(input_data)
    # prepare the solution in the specified output format is
    output_data = str(value) + ' ' + str(1) + '\n'
    output_data += ' '.join(map(str, taken))
    return output_data


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/ks_4_0)')

