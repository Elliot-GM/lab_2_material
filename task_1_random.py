import random
import numpy as np

def randomSearch(map):
    start_pos = 0
    resolved_path = []

    for y in range(len(map)):
        for x in range(len(map[y])):
            if map[y][x] == -2:
                start_pos = [y, x]

    expanded = 0
    pos = start_pos
    resolved_path.append(pos)
    while map[pos[0]][pos[1]] != -3:
        expanded += 1
        directions = [[0, 1], [1, 0], [0, -1], [-1, 0]]
        random.shuffle(directions)

        if pos[0] == 0 or map[pos[0] - 1][pos[1]] == -1:
            directions.remove([-1, 0])
        if pos[0] == len(map) - 1 or map[pos[0] + 1][pos[1]] == -1:
            directions.remove([1, 0])
        if pos[1] == 0 or map[pos[0]][pos[1] - 1] == -1:
            directions.remove([0, -1])
        if pos[1] == len(map[0]) - 1 or map[pos[0]][pos[1] + 1] == -1:
            directions.remove([0, 1])
        pos = [pos[0] + directions[0][0], pos[1] + directions[0][1]]
        resolved_path.append(pos)
    
    print("random expanded", expanded)
    for rp in resolved_path:
        tmp = rp[0]
        rp[0] = rp[1]
        rp[1] = tmp

    return(np.array(resolved_path))
