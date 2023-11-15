import random
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

def BFSNewQueue(map, queue):
    new_queue = []

    for tmp_curent in queue:
        directions = [[0, 1], [1, 0], [0, -1], [-1, 0]]

        if tmp_curent.pos[0] == 0 or map[tmp_curent.pos[0] - 1][tmp_curent.pos[1]] == -1:
            directions.remove([-1, 0])
        if tmp_curent.pos[0] == len(map) - 1 or map[tmp_curent.pos[0] + 1][tmp_curent.pos[1]] == -1:
            directions.remove([1, 0])
        if tmp_curent.pos[1] == 0 or map[tmp_curent.pos[0]][tmp_curent.pos[1] - 1] == -1:
            directions.remove([0, -1])
        if tmp_curent.pos[1] == len(map[0]) - 1 or map[tmp_curent.pos[0]][tmp_curent.pos[1] + 1] == -1:
            directions.remove([0, 1])
        for d in directions:
            new_queue.append(Node([tmp_curent.pos[0] + d[0], tmp_curent.pos[1] + d[1]], tmp_curent))
    return removeDuplicates(new_queue, queue)


def BFSSearch(map):
    resolved_path = []
    queue = []

    for y in range(len(map)):
        for x in range(len(map[y])):
            if map[y][x] == -2:
                queue.append(Node([y, x], None))
                break

    curent_node = queue[0]

    run = True
    while run:
        queue = BFSNewQueue(map, queue)
        for q in queue:
            if map[q.pos[0]][q.pos[1]] == -3:
                curent_node = q
                run = False
                break

    while curent_node.parent != None:
        resolved_path.insert(0, curent_node.pos)
        curent_node = curent_node.parent
    resolved_path.insert(0, curent_node.pos)

    for rp in resolved_path:
        tmp = rp[0]
        rp[0] = rp[1]
        rp[1] = tmp

    return(np.array(resolved_path))
