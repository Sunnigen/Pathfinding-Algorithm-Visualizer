from typing import List, Tuple

# brute_force.py does pathfinding based solely on direction, no real calculations used


def pathfind(start: Tuple[int, int], goal: Tuple[int, int]):
    path = [start]

    curr = start

    goal_x, goal_y = goal

    while curr != goal:

        curr_x, curr_y = curr

        # Check Horizontal
        if curr_x < goal_x:
            curr_x += 1
        elif curr_x > goal_x:
            curr_x -= 1

        # Check Vertical
        if curr_y < goal_y:
            curr_y += 1
        elif curr_y > goal_y:
            curr_y -= 1

        curr = curr_x, curr_y
        path.append(curr)

    # Ensure Start and Goal aren't included in final
    path.remove(start)
    path.remove(goal)

    return path
