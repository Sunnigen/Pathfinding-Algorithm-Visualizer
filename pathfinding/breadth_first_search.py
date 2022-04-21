from __future__ import annotations
from collections import deque
from dataclasses import dataclass, field
from typing import List, Optional, Tuple

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
    parent_node: Node = None

    def __repr__(self):
        return f"{self.c}"


def create_node(curr: Tuple[int, int], parent_node: Optional[Node]) -> Node:
    return Node(curr, parent_node)


def pathfind(graph: List[List[bool]], start: Tuple[int, int], goal: Tuple[int, int]) -> Tuple[List[Tuple[int, int]], List[Tuple[int, int]]]:

    pq: deque[Optional[Node]] = deque()

    pq.append(create_node(start, None))

    closed_nodes: List[Tuple[int, int]] = []

    curr_node: Optional[Node] = None

    goal_found = False

    iterations = 0

    while pq and not goal_found:
        iterations += 1
        if iterations >= MAX_ITERATIONS:
            print(f"ERROR!! ITERATIONS PAST {MAX_ITERATIONS}")
            print(curr_node)

            curr_node = None
            break

        # Pop oldest node in deque
        curr_node = pq.popleft()

        # Add Surrounding Neighbors to deque and Check goal
        for x, y in [[-1, 0], [0, 1], [1, 0], [0, -1]]:
            cx, cy = curr_node.c
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
            else:
                # Add to already visited nodes
                closed_nodes.append((cx, cy))

            # Check if Goal found
            if (cx, cy) == goal:
                curr_node = create_node((cx, cy), curr_node)
                goal_found = True
                break

            # Finally add to Dequeue
            pq.append(create_node((cx, cy), curr_node))

    # No Path Found / Goal not Reached
    try:
        closed_nodes.remove(start)
        closed_nodes.remove(goal)
    except ValueError as e:
        pass
    closed_nodes.reverse()
    if not curr_node or not goal_found:
        return [], closed_nodes

    final_path: List[Tuple[int, int]] = []

    while curr_node is not None:
        final_path.append(curr_node.c)
        curr_node = curr_node.parent_node

    # Remove Start and Goal
    final_path.remove(start)
    final_path.remove(goal)
    return final_path, closed_nodes


if __name__ == "__main__":
    g = [[True for i in range(20)] for j in range(20)]
    start = (0, 0)
    goal = (19, 19)
    print(pathfind(g, start, goal))
