from typing import Dict, List
from puzzle_solver.model import Puzzle, Edge


class GroundTruth:
    def __init__(self, puzzle: Puzzle):
        self.puzzle: Puzzle = puzzle
        self.outer_edges_amount: int = 0
        self.fit_edges: Dict[str, str] = self.find_fitting_edges()

    def _parse_piece_id(self, piece_id: str):
        # Assumes format like p11, p0101, p00010003, etc. (equal-length row and column indices)
        if not piece_id.startswith("p") or len(piece_id) <= 2:
            raise ValueError(f"Invalid piece id format: {piece_id}")

        if piece_id.startswith("piece_"):
            numeric_part = piece_id[6:]
        elif piece_id.startswith("p"):
            numeric_part = piece_id[1:]
        else:
            raise ValueError(f"Invalid piece id format: {piece_id}")

        if len(numeric_part) % 2 != 0:
            raise ValueError("Row and column identifiers must be of equal length.")

        half = len(numeric_part) // 2
        row_str = numeric_part[:half]
        col_str = numeric_part[half:]

        row = int(row_str)
        col = int(col_str)

        return row, col

    def find_fitting_edges(self) -> Dict[str, str]:
        """
        Considering that each puzzle can be seen as a 2D grid of puzzle pieces,
        each right edge should be able to be matched to a a left edge and
        each bottom edge should be able to be matched to fitting top edge,
        with the exception being border pieces.
        Attention: This approach to find fitting edges will only work for a puzzle with a maximum size of 9 by 9 as there
        is no way to determine whether a digit is supposed to be a row or column index.
        E.g.: p11 is row 1 column 1
              p111 could be row 11 column 1, row 1 column 11

        """
        piece_positions = {}
        for piece in self.puzzle.pieces:
            row, col = self._parse_piece_id(piece.id)
            piece_positions[(row, col)] = piece

        matches: Dict[str, List[Edge]] = {
            "right": [],
            "bottom": [],
            "left": [],
            "top": [],
        }
        for (row, col), piece in piece_positions.items():
            # Right neighbor
            right = (row, col + 1)
            if right in piece_positions:
                matches["right"].append(
                    (piece.right_edge, piece_positions[right].left_edge)
                )

            # Bottom neighbor
            bottom = (row + 1, col)
            if bottom in piece_positions:
                matches["bottom"].append(
                    (piece.bottom_edge, piece_positions[bottom].top_edge)
                )

            # Left neighbor
            left = (row, col - 1)
            if left in piece_positions:
                matches["left"].append(
                    (piece.left_edge, piece_positions[left].right_edge)
                )

            # Top neighbor
            top = (row - 1, col)
            if top in piece_positions:
                matches["top"].append(
                    (piece.top_edge, piece_positions[top].bottom_edge)
                )

        result = {
            match[0].id: match[1].id
            for sublist in matches.values()
            for match in sublist
        }
        self.outer_edges_amount = len(self.puzzle.get_edges()) - len(result)
        return result
