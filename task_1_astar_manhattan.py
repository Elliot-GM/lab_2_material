import numpy as np

class Node():
    def __init__(self, parent, position, weight=0, manhattan_distance=0):
        self.parent = parent
        self.position = position
        self.weight = weight
        self.manhattan_distance = manhattan_distance
        self.euristic = weight + manhattan_distance

def inList(list, position):
    for l in list:
        if l.position == position:
            return True
    return False

def myAstar(map, start_pos, end_pos):
    start_node = Node(None, start_pos)
    unused_nodes = [start_node]
    used_nodes = []

    while len(unused_nodes) > 0:
        unused_nodes = sorted(unused_nodes, key=lambda x: x.euristic)
        current_node = unused_nodes[0]

        unused_nodes.pop(0)
        used_nodes.append(current_node)

        if current_node.position[0] == end_pos[0] and current_node.position[1] == end_pos[1]:
            path = []
            while current_node is not None:
                path.append(current_node.position)
                current_node = current_node.parent
            return path

        for new_position in [[0, 1], [1, 0], [0, -1], [-1, 0]]:
            new_node_position = [current_node.position[0] + new_position[0], current_node.position[1] + new_position[1]]

            if new_node_position[0] < 0 or new_node_position[0] >= len(map) or new_node_position[1] < 0 or new_node_position[1] >= len(map[0]):
                continue
            if map[new_node_position[0]][new_node_position[1]] == -1:
                continue
            if inList(used_nodes, new_node_position) == False:
                new_node = Node(current_node, new_node_position, current_node.weight + 1, abs(new_node_position[0] - end_pos[0]) + abs(new_node_position[1] - end_pos[1]))
                if inList(unused_nodes, new_node_position) == False:
                    unused_nodes.append(new_node)

def astarManhattanSearch(map):
    start = 0
    end = 0
    for y in range(len(map)):
        for x in range(len(map[y])):
            if map[y][x] == -2:
                start = [y, x]
            elif map[y][x] == -3:
                end = [y, x]

    resolved_path = myAstar(map, start, end)
    resolved_path.reverse()

    for rp in resolved_path:
        tmp = rp[0]
        rp[0] = rp[1]
        rp[1] = tmp

    return(np.array(resolved_path))
