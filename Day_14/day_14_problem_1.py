import math


def format_input(in_file):
    d = in_file.read().split('\n')
    d = reversed(sorted(d, key=len))
    for line in d:
        ins, out = line.strip().split(' => ')
        out = out.strip()
        amt = int(out.split(' ')[0])
        name = out.split(' ')[1].strip()
        recipes[name] = {name: amt}
        for i in ins.split(', '):
            i = i.strip()
            recipes[name].update({i.split(' ')[1].strip(): int(i.split(' ')[0])})


def print_graph(rows, cols):
    for row in range(rows):
        for col in range(cols):
            print(f"{graph[row][col]:>8}", end='')
        print()



def make_graph():
    for row in range(2, rows):
        for col in range(2, cols - 1):
            if row == col:
                x = row
                graph[row][col + 1] = 0
                while x >= 2:
                    #print(f"The value at {row},{x} is {graph[row][x]}, The value at {x-1},{x} is {graph[x-1][x]}.", row, col, x - 1)
                    if graph[row][x] == '':
                        graph[row][x] = 0
                    graph[row][col + 1] = graph[row][x] * graph[x-1][x] + graph[row][col + 1] 
                    x -= 1
                    #print_graph(rows, cols)
                if row == rows - 1:
                    #graph[row][col] = graph[row][col + 1]
                    #print(graph[row][col + 1], graph[row][1])
                    return
                if graph[row][0] != 'ORE':
                    graph[row][col + 1] = math.ceil(graph[row][col + 1] / graph[row][1])




if __name__ == "__main__":
    recipes = {}
    with open("Day_14/Data/day-14.txt", 'r') as in_file:
        format_input(in_file)

    cols = len(recipes)+3
    rows = len(recipes)+2
    graph = [['' for col in range(cols)] for row in range(rows)]

    row = 1
    col = 2
    graph[0][0] = '-  '
    graph[0][1] = 'Y  '
    for key in recipes:
        graph[row][0] = key
        graph[row][1] = recipes[key][key]
        graph[0][col] = key
        row+=1
        col+=1

    for row in range(1, rows-1):
        for col in range(2, cols-1):
            if graph[0][col] in recipes[graph[row][0]]:
                graph[col-1][row+1] = recipes[graph[row][0]][graph[0][col]]
    print()

    for col in range(cols):
        if graph[0][col] in recipes:
            if 'ORE' in recipes[graph[0][col]]:
                graph[rows-1][col] = recipes[graph[0][col]]['ORE']
        if col+1 < cols:
            graph[col][col+1] = 'x'

    graph[1][2] = graph[1][1]
    graph[0][cols-1] = 'ORE'
    graph[rows-1][0] = 'ORE'
    graph[rows-1][1] = 1
    make_graph()
    print_graph(rows, cols)

    print(graph[rows-1][cols-1])