import numpy as np

class Node:
    def __init__(self, pos, parent):
        self.pos = pos
        self.parent = parent

def removeDuplicates(queue, other):
    seen_positions = {}
    unique_nodes = []

    for q in queue:
        position = tuple(q.pos)

        if position not in seen_positions:
            seen_positions[position] = True
            unique_nodes.append(q)

    set1_positions = set(tuple(point.pos) for point in other)

    filtered = [point for point in unique_nodes if tuple(point.pos) not in set1_positions]

    return filtered

def euclideanDistance(node, pos2):
    return np.sqrt((node.pos[0] - pos2[0])**2 + (node.pos[1] - pos2[1])**2)

def greedyAddQueue(map, queue, visited, objetif_pos):
    directions = [[0, 1], [1, 0], [0, -1], [-1, 0]]

    if queue[0].pos[0] == 0 or map[queue[0].pos[0] - 1][queue[0].pos[1]] == -1:
        directions.remove([-1, 0])
    if queue[0].pos[0] == len(map) - 1 or map[queue[0].pos[0] + 1][queue[0].pos[1]] == -1:
        directions.remove([1, 0])
    if queue[0].pos[1] == 0 or map[queue[0].pos[0]][queue[0].pos[1] - 1] == -1:
        directions.remove([0, -1])
    if queue[0].pos[1] == len(map[0]) - 1 or map[queue[0].pos[0]][queue[0].pos[1] + 1] == -1:
        directions.remove([0, 1])
    lil_queue = []
    for d in directions:
        lil_queue.append(Node([queue[0].pos[0] + d[0], queue[0].pos[1] + d[1]], queue[0]))
    queue = lil_queue + queue
    queue = sorted(queue, key=lambda x: euclideanDistance(x, objetif_pos))

    return removeDuplicates(queue, visited)

def greedySearch(map):
    objetif_pos = 0
    resolved_path = []
    queue = []
    visited = []

    for y in range(len(map)):
        for x in range(len(map[y])):
            if map[y][x] == -2:
                queue.append(Node([y, x], None))
                break
            elif map[y][x] == -3:
                objetif_pos = [y, x]
                break

    curent_node = queue[0]
    expanded = 0

    while True:
        expanded += 1
        if map[queue[0].pos[0]][queue[0].pos[1]] == -3:
            curent_node = queue[0]
            break
        visited.append(queue[0])
        queue = greedyAddQueue(map, queue, visited, objetif_pos)
    
    print("greedy expanded", expanded)

    while curent_node.parent != None:
        resolved_path.insert(0, curent_node.pos)
        curent_node = curent_node.parent
    resolved_path.insert(0, curent_node.pos)

    for rp in resolved_path:
        tmp = rp[0]
        rp[0] = rp[1]
        rp[1] = tmp

    return(np.array(resolved_path))
