''' --- Day 14: Space Stoichiometry ---
As you approach the rings of Saturn, your ship's low fuel indicator turns on.
There isn't any fuel here, but the rings have plenty of raw material. Perhaps
your ship's Inter-Stellar Refinery Union brand nanofactory can turn these raw
materials into fuel.

You ask the nanofactory to produce a list of the reactions it can perform that
are relevant to this process (your puzzle input). Every reaction turns some
quantities of specific input chemicals into some quantity of an output
chemical. Almost every chemical is produced by exactly one reaction; the only
exception, ORE, is the raw material input to the entire process and is not
produced by a reaction.

You just need to know how much ORE you'll need to collect before you can
produce one unit of FUEL.

Each reaction gives specific quantities for its inputs and output; reactions
cannot be partially run, so only whole integer multiples of these quantities
can be used. (It's okay to have leftover chemicals when you're done, though.)
For example, the reaction 1 A, 2 B, 3 C => 2 D means that exactly 2 units of
chemical D can be produced by consuming exactly 1 A, 2 B and 3 C. You can run
the full reaction as many times as necessary; for example, you could produce
10 D by consuming 5 A, 10 B, and 15 C.

Suppose your nanofactory produces the following list of reactions:

    10 ORE => 10 A
    1 ORE => 1 B
    7 A, 1 B => 1 C
    7 A, 1 C => 1 D
    7 A, 1 D => 1 E
    7 A, 1 E => 1 FUEL

The first two reactions use only ORE as inputs; they indicate that you can
produce as much of chemical A as you want (in increments of 10 units, each 10
costing 10 ORE) and as much of chemical B as you want (each costing 1 ORE). To
produce 1 FUEL, a total of 31 ORE is required: 1 ORE to produce 1 B, then 30
more ORE to produce the 7 + 7 + 7 + 7 = 28 A (with 2 extra A wasted) required
in the reactions to convert the B into C, C into D, D into E, and finally E
into FUEL. (30 A is produced because its reaction requires that it is created
in increments of 10.)

Or, suppose you have the following list of reactions:

    9 ORE => 2 A
    8 ORE => 3 B
    7 ORE => 5 C
    3 A, 4 B => 1 AB
    5 B, 7 C => 1 BC
    4 C, 1 A => 1 CA
    2 AB, 3 BC, 4 CA => 1 FUEL

The above list of reactions requires 165 ORE to produce 1 FUEL:

    --  Consume 45 ORE to produce 10 A.
    --  Consume 64 ORE to produce 24 B.
    --  Consume 56 ORE to produce 40 C.
    --  Consume 6 A, 8 B to produce 2 AB.
    --  Consume 15 B, 21 C to produce 3 BC.
    --  Consume 16 C, 4 A to produce 4 CA.
    --  Consume 2 AB, 3 BC, 4 CA to produce 1 FUEL.

Here are some larger examples:

--  13312 ORE for 1 FUEL:

    157 ORE => 5 NZVS
    165 ORE => 6 DCFZ
    44 XJWVT, 5 KHKGT, 1 QDVJ, 29 NZVS, 9 GPVTF, 48 HKGWZ => 1 FUEL
    12 HKGWZ, 1 GPVTF, 8 PSHF => 9 QDVJ
    179 ORE => 7 PSHF
    177 ORE => 5 HKGWZ
    7 DCFZ, 7 PSHF => 2 XJWVT
    165 ORE => 2 GPVTF
    3 DCFZ, 7 NZVS, 5 HKGWZ, 10 PSHF => 8 KHKGT

--  180697 ORE for 1 FUEL:

    2 VPVL, 7 FWMGM, 2 CXFTF, 11 MNCFX => 1 STKFG
    17 NVRVD, 3 JNWZP => 8 VPVL
    53 STKFG, 6 MNCFX, 46 VJHF, 81 HVMC, 68 CXFTF, 25 GNMV => 1 FUEL
    22 VJHF, 37 MNCFX => 5 FWMGM
    139 ORE => 4 NVRVD
    144 ORE => 7 JNWZP
    5 MNCFX, 7 RFSQX, 2 FWMGM, 2 VPVL, 19 CXFTF => 3 HVMC
    5 VJHF, 7 MNCFX, 9 VPVL, 37 CXFTF => 6 GNMV
    145 ORE => 6 MNCFX
    1 NVRVD => 8 CXFTF
    1 VJHF, 6 MNCFX => 4 RFSQX
    176 ORE => 6 VJHF

--  2210736 ORE for 1 FUEL:

    171 ORE => 8 CNZTR
    7 ZLQW, 3 BMBT, 9 XCVML, 26 XMNCP, 1 WPTQ, 2 MZWV, 1 RJRHP => 4 PLWSL
    114 ORE => 4 BHXH
    14 VRPVC => 6 BMBT
    6 BHXH, 18 KTJDG, 12 WPTQ, 7 PLWSL, 31 FHTLT, 37 ZDVW => 1 FUEL
    6 WPTQ, 2 BMBT, 8 ZLQW, 18 KTJDG, 1 XMNCP, 6 MZWV, 1 RJRHP => 6 FHTLT
    15 XDBXC, 2 LTCX, 1 VRPVC => 6 ZLQW
    13 WPTQ, 10 LTCX, 3 RJRHP, 14 XMNCP, 2 MZWV, 1 ZLQW => 1 ZDVW
    5 BMBT => 4 WPTQ
    189 ORE => 9 KTJDG
    1 MZWV, 17 XDBXC, 3 XCVML => 2 XMNCP
    12 VRPVC, 27 CNZTR => 2 XDBXC
    15 KTJDG, 12 BHXH => 5 XCVML
    3 BHXH, 2 VRPVC => 7 MZWV
    121 ORE => 7 VRPVC
    7 XCVML => 6 RJRHP
    5 BHXH, 4 VRPVC => 5 LTCX

Given the list of reactions in your puzzle input, what is the minimum amount
of ORE required to produce exactly 1 FUEL?
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
    fi = open("Day_14/graph.txt", 'w')
    s = ''
    for row in range(rows):
        for col in range(cols):
            if graph[row][col] == 0:
                graph[row][col] = '.'
            if (col == 1 and row != 0) or (row == col - 1):
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
    graph[0][1] = 'Yeild '


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
                    return
                if graph[row][0] != 'ORE':
                    graph[row][col + 1] = math.ceil(
                            graph[row][col + 1] / graph[row][1])


if __name__ == "__main__":
    with open("Day_14/Data/day-14.txt", 'r') as in_file:
        recipes = format_input(in_file)
    order_indexes = topo_sort(recipes)
    cols = len(recipes)+3
    rows = len(recipes)+2
    graph = [['' for col in range(cols)] for row in range(rows)]
    make_graph(graph, recipes, order_indexes, rows, cols)
    print_graph(rows, cols)
    print(
        f"The total number of ore needed for 1 fuel is {graph[rows-1][cols-1]}"
        )
    # Your puzzle answer was 387001
