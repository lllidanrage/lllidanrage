# COMP30024 Artificial Intelligence, Semester 1 2025
# Project Part A: Single Player Freckers
import subprocess
from collections import deque

from .core import CellState, Coord, Direction, MoveAction
from .utils import render_board


def get_all_movements(board: dict[Coord, CellState], position: Coord) -> list[list[Direction]]:

    def valid_position(pos, dir):
        return 0 <= pos.r + dir.r <= 7 and 0 <= pos.c + dir.c <= 7

    movements = []

    directions = [
        Direction.Down,
        Direction.DownLeft,
        Direction.DownRight,
        Direction.Left,
        Direction.Right
    ]

    for direction in directions:
        try:
            possible_position = position + direction
        except ValueError:
            continue
        if (valid_position(position, direction) and possible_position in board and
                board[possible_position] not in (CellState.RED, CellState.BLUE)):
            movements.append(direction)

    visited = set()

    def dfs(pos: Coord, path: list[Direction]):
        if path:
            movements.append(path.copy())

        for direction in directions:
            try:
                jumped_pos = pos + direction
            except ValueError:
                continue
            if jumped_pos not in board or board[jumped_pos] not in (CellState.RED, CellState.BLUE):
                continue

            try:
                new_pos = jumped_pos + direction
            except ValueError:
                continue
            if (valid_position(jumped_pos, direction) and new_pos in board and
                    board[new_pos] not in (CellState.RED, CellState.BLUE)):
                new_path = path + [direction]
                if new_pos not in visited:
                    visited.add(new_pos)
                    dfs(new_pos, new_path)
                    visited.remove(new_pos)

    dfs(position, [])
    return movements


def search(
        board: dict[Coord, CellState]
) -> list[MoveAction] | None:
    """
    This is the entry point for your submission. You should modify this
    function to solve the search problem discussed in the Part A specification.
    See `core.py` for information on the types being used here.

    Parameters:
        `board`: a dictionary representing the initial board state, mapping
            coordinates to "player colours". The keys are `Coord` instances,
            and the values are `CellState` instances which can be one of
            `CellState.RED`, `CellState.BLUE`, or `CellState.LILY_PAD`.

    Returns:
        A list of "move actions" as MoveAction instances, or `None` if no
        solution is possible.
    """

    # The render_board() function is handy for debugging. It will print out a
    # board state in a human-readable format. If your terminal supports ANSI
    # codes, set the `ansi` flag to True to print a colour-coded version!
    print(render_board(board, ansi=True))

    # Do some impressive AI stuff here to find the solution...
    # ...
    # ... (your solution goes here!)
    # ...

    start_coord = None
    aim_coord = []

    for coord, state in board.items():
        if state == CellState.RED:
            start_coord = coord
        elif state == CellState.LILY_PAD and coord.r == 7:
            aim_coord.append(coord)

    if not start_coord or not aim_coord:
        return None

    queue = deque()
    queue.append((start_coord, []))

    visited = set()
    visited.add(start_coord)

    # BFS
    while queue:
        current_coord, action = queue.popleft()

        if current_coord.r == 7 and current_coord in aim_coord:
            return action

        movements = get_all_movements(board, current_coord)
        for movement in movements:
            next_coord = None
            if isinstance(movement, Direction):
                next_coord = current_coord + movement
            else:
                for direction in movement:
                    next_coord = current_coord + direction + direction

            if next_coord not in visited:
                visited.add(next_coord)
                movement = [movement] if isinstance(movement, Direction) else movement

                new_action = MoveAction(current_coord, movement)

                new_path = action + [new_action]

                queue.append((next_coord, new_path))

    return None

    # Here we're returning "hardcoded" actions as an example of the expected
    # output format. Of course, you should instead return the result of your
    # search algorithm. Remember: if no solution is possible for a given input,
    # return `None` instead of a list.
    # return [
    #     MoveAction(Coord(0, 5), [Direction.Down]),
    #     MoveAction(Coord(1, 5), [Direction.DownLeft]),
    #     MoveAction(Coord(3, 3), [Direction.Left]),
    #     MoveAction(Coord(3, 2), [Direction.Down, Direction.Right]),
    #     MoveAction(Coord(5, 4), [Direction.Down]),
    #     MoveAction(Coord(6, 4), [Direction.Down]),
    # ]
