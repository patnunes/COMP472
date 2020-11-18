import time
import node
def uniform_cost(puzzle):
    start = time.time()
    node = Node(puzzle())
    openlist = []
    openlist.append(node)
    closedlist = []
    while openlist:
        node = openlist.pop()
        if puzzle.goal_test(node.state):
            print(len(closedlist), "paths have been expanded and", len(openlist), "paths remain in the openlist")
            return
        closedlist.append(node.state)
        for child in node.expand(puzzle):
            if child.state not in closedlist and child not in openlist:
                openlist.append(child)
            elif child in openlist:
                if child.g < openlist[child.g]:
                    del openlist[child]
                    openlist.append(child)
                    openlist.sort(node.g)
        
        now = time.time()
        if (now - start) > 60:
            return
    