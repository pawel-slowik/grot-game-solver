#!/usr/bin/env python3

from typing import NamedTuple, Iterable, Sequence

class Position(NamedTuple):
    row: int
    column: int

Path = Sequence[Position]

class Move(NamedTuple):
    vertical: int
    horizontal: int

Board = Sequence[Sequence[str]]

def find_best_path(board: Board) -> Path:
    all_paths = map(lambda position: travel(board, position), list_positions(board))
    return sorted(all_paths, key=path_weight)[-1]

def path_weight(path: Path) -> int:
    # skip already visited fields when choosing the best path
    return len(set(path))

def travel(board: Board, start_position: Position) -> Path:
    position = start_position
    path = []
    while True:
        path.append(position)
        new_position = move(board, position, path)
        if not in_board(board, new_position):
            break
        position = new_position
    return path

def move(board: Board, position: Position, path: Path) -> Position:
    delta = compute_next_move(board, position, path[:-1])
    return Position(
        row=position.row + delta.vertical,
        column=position.column + delta.horizontal,
    )

def compute_next_move(board: Board, position: Position, path: Path) -> Move:
    direction_map = {
        'u': Move(vertical=-1, horizontal=0),
        'd': Move(vertical=1, horizontal=0),
        'r': Move(vertical=0, horizontal=1),
        'l': Move(vertical=0, horizontal=-1),
    }
    if position in path:
        # already visited / cleared, continue in the same direction
        previous_position = path[-1]
        return Move(
            vertical=position.row - previous_position.row,
            horizontal=position.column - previous_position.column,
        )
    return direction_map[board[position.row][position.column]]

def in_board(board: Board, position: Position) -> bool:
    return position in list_positions(board)

def list_positions(board: Board) -> Iterable[Position]:
    for row_number, row in enumerate(board):
        for column_number, _ in enumerate(row):
            yield Position(row=row_number, column=column_number)

def main() -> None:
    sample = [
        ['u', 'd', 'u', 'u'], # ↑ ↓ ↑ ↑
        ['u', 'r', 'l', 'l'], # ↑ → ← ←
        ['u', 'u', 'l', 'u'], # ↑ ↑ ← ↑
        ['l', 'd', 'u', 'l'], # ← ↓ ↑ ←
    ]
    print(find_best_path(sample)[0])

if __name__ == "__main__":
    main()
