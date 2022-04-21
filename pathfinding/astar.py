from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Optional, Tuple
from queue import PriorityQueue

"""
f = g + h
f -> total cost to travel to node
g -> distance from start node to current node
h -> heuristic, pythagorean theorem, distance between current node and goal node
"""

MAX_ITERATIONS = 5000

@dataclass
class Node:
    c: Tuple[int, int]
    parent_node: Node
    g: int
    h: int

    @property
    def f(self):
        return self.g + self.h

    def __repr__(self):
        return f"Node at: {self.c}, f: {self.f}, g: {self.g}, h: {self.h}"


@dataclass(order=True)
class PrioritizedItem:
    priority: int
    item: Node = field(compare=False)


def calculate_distance(c1: Tuple[int, int], c2: Tuple[int, int]) -> int:
    return (c1[0] - c2[0]) ** 2 + (c1[1] - c2[1]) ** 2


def pathfind(graph: List[List[bool]], start: Tuple[int, int], goal: Tuple[int, int]) -> Tuple[List[Tuple[int, int]], List[Tuple[int, int]]]:
    pq: PriorityQueue[Node] = PriorityQueue()

    add_to_pqueue(pq, create_node(curr=start,
                                  dist=0,
                                  goal=goal,
                                  parent_node=None))

    closed_nodes: List[Tuple[int, int]] = []

    curr_node: Optional[PrioritizedItem] = None

    goal_found = False

    iterations = 0

    while not pq.empty():

        if goal_found:
            break
        iterations += 1
        if iterations >= MAX_ITERATIONS:
            print(f"ERROR!! ITERATIONS PAST {MAX_ITERATIONS}")
            print(curr_node)
            curr_node = None
            break

        # Obtain node with lowest f score
        curr_node = pq.get()

        # Add Surrounding Neighbors to PriorityQueue
        for x, y in [[-1, 0], [0, 1], [1, 0], [0, -1]]:
            cx, cy = curr_node.item.c
            cx += x
            cy += y

            if goal_found:
                break

            # Check if Still within boundary
            if cx < 0 or cx > len(graph) - 1 or cy < 0 or cy > len(graph[0]) - 1:
                continue

            # Check there is no Obstacle
            if not graph[cx][cy]:
                continue

            # Check if already visited
            if (cx, cy) in closed_nodes:
                continue

            # Add to already visited nodes
            closed_nodes.append((cx, cy))

            # Check if at Goal
            if (cx, cy) == goal:
                curr_node = curr_node.item
                goal_found = True
                break

            # Finally add to PriorityQueue
            add_to_pqueue(pq, create_node(curr=(cx, cy),
                                          dist=curr_node.item.g + 1,
                                          goal=goal,
                                          parent_node=curr_node.item)
            )

    # No Path Found / Goal not Reached
    try:
        closed_nodes.reverse()
        closed_nodes.remove(start)
        closed_nodes.remove(goal)
    except:
        pass
    if not curr_node or not goal_found:
        return [], closed_nodes

    final_path: List[Tuple[int, int]] = []

    while curr_node:
        final_path.append(curr_node.c)
        curr_node = curr_node.parent_node

    # Remove Start and Goal
    try:
        final_path.remove(start)
        final_path.remove(goal)
    except ValueError:
        pass
    return final_path, closed_nodes


def create_node(curr: Tuple[int, int], dist: int, goal: Tuple[int, int], parent_node: Optional[Node]) -> Node:
    return Node(curr, parent_node, dist, calculate_distance(curr, goal))


def add_to_pqueue(p: PriorityQueue, node: Node):
    p.put(PrioritizedItem(node.f, node))


def astar_test():
    import random
    p = PriorityQueue()
    s = (0, 0)
    g = (20, 20)
    add_to_pqueue(p, create_node(s, 0, g))

    for i in range(10):
        c = (random.randint(1, 19), random.randint(1, 19))
        add_to_pqueue(p, create_node(c, calculate_distance(s, c), g))

    add_to_pqueue(p, create_node((20, 19), calculate_distance((20, 19), s), g))
    # add_to_pqueue(p, create_node((8, 8), 8, g))


    while p:
        print(p.get().item)


if __name__ == "__main__":
    # astar_test()
    g = [[True for i in range(20)] for j in range(20)]



    start = (0, 0)
    goal = (19, 19)
    print(pathfind(g, start, goal))
