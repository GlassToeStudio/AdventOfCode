''' --- Part Two ---
After collecting ORE for a while, you check your cargo hold: 1 trillion
(1000000000000) units of ORE.

With that much ore, given the examples above:

--  The 13312 ORE-per-FUEL example could produce 82892753 FUEL.
--  The 180697 ORE-per-FUEL example could produce 5586022 FUEL.
--  The 2210736 ORE-per-FUEL example could produce 460664 FUEL.

Given 1 trillion ORE, what is the maximum amount of FUEL you can produce?
'''

import math


def format_input(in_file):
    unordered_recipes = {}
    d = in_file.read().split('\n')
    for line in d:
        ins, out = line.strip().split(' => ')
        out = out.strip()
        amt = int(out.split(' ')[0])
        name = out.split(' ')[1].strip()
        unordered_recipes[name] = {name: amt}
        for i in ins.split(', '):
            i = i.strip()
            unordered_recipes[name].update(
                {i.split(' ')[1].strip(): int(i.split(' ')[0])})
    return unordered_recipes


def topo_sort(recipes):
    order_index = [0 for x in range(len(recipes))]
    n = len(order_index)-1
    while n > 0:
        n, order_index = dfs(recipes, 'FUEL', n, order_index)
    return order_index


def dfs(recipes, name, i, ordered_dict):
    if name != 'ORE':
        for k in recipes[name]:
            if k != name and k not in ordered_dict:
                if k == 'ORE':
                    ordered_dict[i] = name
                    return i - 1, ordered_dict
                else:
                    i, ordered_dict = dfs(recipes, k, i, ordered_dict)
        ordered_dict[i] = name
        i -= 1
    return i, ordered_dict


def print_graph(rows, cols):
    fi = open("Day_14/graph-2.txt", 'w')
    s = ''
    for row in range(rows):
        for col in range(cols):
            if graph[row][col] == 0:
                graph[row][col] = '.'
            if (col == 1 and row != 0) or (row == col - 1) and row != rows - 1:
                graph[row][col] = f"| {graph[row][col]} |"
            s += f" {graph[row][col]:>8}"
        s += '\n'
    print(s, file=fi)


def add_headers(graph, recipes, order_index):
    row = 1
    col = 2
    graph[0][0] = '-  '
    graph[0][1] = 'Y  '
    for key in order_index:
        graph[0][col] = key
        graph[row][0] = key
        graph[row][1] = recipes[key][key]
        row += 1
        col += 1


def add_values(graph, recipes):
    for row in range(1, rows-1):
        for col in range(2, cols-1):
            if graph[0][col] in recipes[graph[row][0]]:
                graph[col-1][row+1] = recipes[graph[row][0]][graph[0][col]]


def add_ore(graph, recipes):
    for col in range(cols):
        if graph[0][col] in recipes:
            if 'ORE' in recipes[graph[0][col]]:
                graph[rows-1][col] = recipes[graph[0][col]]['ORE']
        if col+1 < cols:
            graph[col][col+1] = 0

    graph[1][2] = graph[1][1]
    graph[0][cols-1] = 'ORE'
    graph[rows-1][0] = 'ORE'
    graph[rows-1][1] = 1
    graph[0][1] = 'Yeild'


def make_graph(graph, recipes, order_index, rows, cols):
    add_headers(graph, recipes, order_index)
    add_values(graph, recipes)
    add_ore(graph, recipes)
    for row in range(2, rows):
        for col in range(2, cols - 1):
            if row == col:
                x = row
                graph[row][col + 1] = 0
                while x >= 2:
                    if graph[row][x] == '':
                        graph[row][x] = 0
                    graph[row][col + 1] = graph[row][x] * \
                        graph[x-1][x] + graph[row][col + 1]
                    x -= 1
                if row == rows - 1:
                    return graph[rows-1][cols-1]
                if graph[row][0] != 'ORE':
                    graph[row][col + 1] = math.ceil(
                            graph[row][col + 1] / graph[row][1])


def get_ore_requirements(graph):
    ore_chems = {}
    # all columns
    cols = len(graph[0]) - 1
    rows = len(graph) - 1
    for i in range(cols):
        if isinstance(graph[rows][i], int):
            ore_chems[graph[0][i]] = \
                graph[rows][i] * int(graph[i - 1][i].split('|')[1])
    print(ore_chems)
    return ore_chems


if __name__ == "__main__":
    with open("Day_14/Data/day-14.txt", 'r') as in_file:
        recipes = format_input(in_file)
    order_indexes = topo_sort(recipes)
    print(recipes['FUEL']['FUEL'])
    cols = len(recipes)+3
    rows = len(recipes)+2
    graph = [['' for col in range(cols)] for row in range(rows)]
    ore = make_graph(graph, recipes, order_indexes, rows, cols)
    # Cheap and dirty
    i = 3412427
    while ore < 1000000000000:
        i += 1
        recipes['FUEL']['FUEL'] = i
        ore = make_graph(graph, recipes, order_indexes, rows, cols)

    recipes['FUEL']['FUEL'] = i - 1
    ore = make_graph(graph, recipes, order_indexes, rows, cols)
    print_graph(rows, cols)

    print(
        "The total number of fuel created "
        f"from 1,000,000,000,000 ore is {i - 1}"
        )
    # Your puzzle answer was 3412429
