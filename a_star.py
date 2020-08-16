class Node:
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position
        self.g = 0  # Distance between current and starting node
        self.h = 0  # Heuristic distance found using pythagorean theorem
        self.f = 0  # Total cost of a node (h + g)

    def __eq__(self, other):
        # Checking if positions are same
        return self.position == other.position


def a_star(grid, start, end):
    """
    Finds the shortest path using heuristics. Starts with a node and checks adjacent ones, seeing which one is most
    likely to form the shortest path to target. This is done by calculating euclidean distance from current node
    to ending cell.
    :param grid: Board
    :param start: Starting cell
    :param end: Ending cell
    :return: Path from start to end
    """

    # Starting node
    start_node = Node(None, start)
    start_node.g = start_node.f = start_node.h = 0

    # Ending node
    end_node = Node(None, end)
    end_node.g = end_node.f = end_node.h = 0

    open_list = []
    closed_list = []

    open_list.append(start_node)  # Append starting node to open list

    # Loop through open list until end is found
    while open_list:
        # Get current node
        current = open_list[0]
        index = 0

        # Looping through each node and trying ones that "cost less"
        for i, j in enumerate(open_list):
            if j.f < current.f:
                current = j
                index = i

        # Moving node to closed list
        open_list.pop(index)
        closed_list.append(current)

        # If end goal is reached
        if current == end_node:
            path = []
            c = current
            while c is not None:
                # Going through all each parent to each node and appending it to path
                path.append(c.position)
                c = c.parent
            return path[::-1]  # Return the reversed path

        children = []  # Children of the current node
        for pos in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            node_pos = (current.position[0] + pos[0], current.position[1] + pos[1])
            if node_pos[0] > len(grid)-1 or node_pos[0] < 0 or node_pos[1] > (len(grid[len(grid)-1])-1) or \
                    node_pos[1] < 0:  # Checking if cell is in the boundaries
                continue

            if not grid[node_pos[0]][node_pos[1]]:  # Skip over cell if it is invalid
                continue

            # Appending child node to children
            node = Node(current, node_pos)
            children.append(node)

        for child in children:
            # Ensuring child is not in closed list
            cont = False
            for c in closed_list:
                if child == c:  # Skip over if child is already in closed list
                    cont = True
                    break

            if cont:
                continue

            child.g = current.g + 1  # Increment distance from start to current
            child.h = ((child.position[0] - end_node.position[0]) ** 2) + \
                      ((child.position[1] - end_node.position[1]) ** 2)  # Euclidean heuristic distance
            child.f = child.g + child.h  # Update cost of child

            for n in open_list:
                if child == n and child.g > n.g:
                    # If child's g value is higher than that of the one in the open list, skip over it
                    cont = True
                    break

            if cont:
                continue

            open_list.append(child)

