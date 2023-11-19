import numpy as np

class Node():
    def __init__(self, parent, position, weight=0, euclidean_distance=0):
        self.parent = parent
        self.position = position
        self.weight = weight
        self.euclidean_distance = euclidean_distance
        self.euristic = weight + euclidean_distance

def inList(list, position):
    for l in list:
        if l.position == position:
            return True
    return False

def myAstar(map, start_pos, end_pos):
    start_node = Node(None, start_pos)
    unused_nodes = [start_node]
    used_nodes = []
    expanded = 0

    while len(unused_nodes) > 0:
        expanded += 1
        unused_nodes = sorted(unused_nodes, key=lambda x: x.euristic)
        current_node = unused_nodes[0]

        unused_nodes.pop(0)
        used_nodes.append(current_node)

        if current_node.position[0] == end_pos[0] and current_node.position[1] == end_pos[1]:
            path = []
            while current_node is not None:
                path.append(current_node.position)
                current_node = current_node.parent
            print("A* heuristic expanded", expanded)
            return path

        for new_position in [[0, 1], [1, 0], [0, -1], [-1, 0]]:
            new_node_position = [current_node.position[0] + new_position[0], current_node.position[1] + new_position[1]]

            if new_node_position[0] < 0 or new_node_position[0] >= len(map) or new_node_position[1] < 0 or new_node_position[1] >= len(map[0]):
                continue
            if map[new_node_position[0]][new_node_position[1]] == -1:
                continue
            if inList(used_nodes, new_node_position) == False:
                new_node = Node(current_node, new_node_position, current_node.weight + 1, np.sqrt((new_node_position[0] - end_pos[0])**2 + (new_node_position[1] - end_pos[1])**2))
                if inList(unused_nodes, new_node_position) == False:
                    unused_nodes.append(new_node)

def astarHeuristicSearch(map):
    start = 0
    end = 0
    for y in range(len(map)):
        for x in range(len(map[y])):
            if map[y][x] == -2:
                start = [y, x]
            elif map[y][x] == -3:
                end = [y, x]
    up = True if end[0] < len(map) / 2 else False
    middle_start_pos = [0, start[1]]
    middle_end_pos = [0, end[1]]

    if up:
        middle_start_pos[0] = 0
        middle_end_pos[0] = 0
        while middle_start_pos[0] < len(map) and map[middle_start_pos[0]][middle_start_pos[1]] == -1:
            middle_start_pos[0] += 1
        while middle_end_pos[0] < len(map) and map[middle_end_pos[0]][middle_end_pos[1]] == -1:
            middle_end_pos[0] += 1
    else:
        middle_start_pos[0] = len(map) - 1
        middle_end_pos[0] = len(map) - 1
        while middle_start_pos[0] >= 0 and map[middle_start_pos[0]][middle_start_pos[1]] == -1:
            middle_start_pos[0] -= 1
        while middle_end_pos[0] >= 0 and map[middle_end_pos[0]][middle_end_pos[1]] == -1:
            middle_end_pos[0] -= 1

    resolved_path_one = myAstar(map, start, middle_start_pos)
    resolved_path_two = myAstar(map, middle_start_pos, middle_end_pos)
    resolved_path_three = myAstar(map, middle_end_pos, end)
    resolved_path_one.reverse()
    resolved_path_two.reverse()
    resolved_path_three.reverse()
    resolved_path = resolved_path_one + resolved_path_two + resolved_path_three

    for rp in resolved_path:
        tmp = rp[0]
        rp[0] = rp[1]
        rp[1] = tmp

    return(np.array(resolved_path))
