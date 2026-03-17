from puzzle_solver.model import PuzzlePiece


def assert_sample1(solved_puzzle: list[list[PuzzlePiece]]):
    ground_truth = []
    for i in range(7):
        ground_truth.append([ 11 * j +i for j in range(5)])
    
    assert(ground_truth, solved_puzzle)

def assert_puzzle_solved(solved_puzzle: list[list[PuzzlePiece]], rows: int, cols: int):
    solved = False
    template = get_template(rows, cols)
    piece_ids = get_piece_ids(solved_puzzle)
    for _ in range(4):
        template = rotate_2d_matrix(template)
        if template == piece_ids:
            solved = True
            break
    assert solved, f"failed to solve puzzle: {piece_ids}"


def get_template(rows: int, cols: int) -> list[list[str]]:
    template: list[list[str]] = []
    for i in range(rows):
        row: list[str] = []
        for j in range(cols):
            row.append(str(i * cols + j))
        template.append(row)
    return template


def rotate_2d_matrix(matrix: list[list[str]]) -> list[list[str]]:
    # Transpose the matrix
    transposed = [list(row) for row in zip(*matrix)]
    # Reverse each row to rotate 90 degrees
    rotated = [row[::-1] for row in transposed]
    return rotated


def get_piece_ids(solved_puzzle: list[list[PuzzlePiece]]) -> list[list[str]]:
    return [[piece.id for piece in row] for row in solved_puzzle]
