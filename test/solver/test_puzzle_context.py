import unittest
from puzzle_solver.solver.puzzle_context import PuzzleContext
from puzzle_solver.test_data import get_puzzle


class TestPuzzleContext(unittest.TestCase):
    def test_get_piece_context(self):
        puzzle = get_puzzle(3, 3, 100)
        puzzle_context = PuzzleContext(16)
        puzzle_context.add_piece_at(puzzle.pieces[0], 0, 1)
        puzzle_context.add_piece_at(puzzle.pieces[1], 1, 0)
        context = puzzle_context.get_context(1, 1)
        assert context.bottom_edge == puzzle.pieces[1].top_edge
        assert context.left_edge == puzzle.pieces[0].right_edge
        assert context.right_edge is None
        assert context.top_edge is None
