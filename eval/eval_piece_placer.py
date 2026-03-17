import random
import unittest

from eval.util import plot_placed_puzzle
from puzzle_solver.model import PuzzlePiece
from puzzle_solver.piece_placer.piece_placer import PiecePlacer
from puzzle_solver.test_data.generator import Generator


class TestEvalPiecePlacer(unittest.TestCase):
    def test_piece_placer(self):
        random.seed(42)
        rows, cols = 9, 9  # Adjust these values as needed
        puzzle = Generator(rows, cols).generate()
        solved_puzzle: list[list[PuzzlePiece]] = []
        for row_index in range(rows - 1, -1, -1):
            solved_puzzle.append([])
            for col_index in range(cols):
                solved_puzzle[-1].append(puzzle.pieces[row_index * cols + col_index])


        placed_pieces = PiecePlacer(puzzle, 0.25).generate_piece_positions(solved_puzzle)
        plot_placed_puzzle(placed_pieces, puzzle.pieces, "piece-placer-eval")
