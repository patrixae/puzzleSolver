import unittest

from eval.util import plot_placed_puzzle
from puzzle_solver.file_parser import get_puzzle_104
from puzzle_solver.model import PuzzlePiece
from puzzle_solver.piece_placer.lin_alg import LinProgPiecePlacer


class TestEvalPiecePlacerRealData(unittest.TestCase):
    def test_piece_placer(self):
        puzzle = get_puzzle_104()
        solved_puzzle: list[list[PuzzlePiece]] = list()
        for i in range(8):
            solved_puzzle.append(list())
            for j in range(13):
                solved_puzzle[-1].append(puzzle.pieces[i * 13 + j])

        placed_pieces = LinProgPiecePlacer(puzzle).generate_piece_positions(
            solved_puzzle
        )
        plot_placed_puzzle(placed_pieces, puzzle, "linprog-piece-placer-eval-real-data")
