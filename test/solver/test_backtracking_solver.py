import random
import unittest
from puzzle_solver.edge_matcher.edge_match_matrix import create_edge_match_matrices
from puzzle_solver.piece_matcher.piece_matcher import PieceMatcher
from puzzle_solver.edge_matcher.edge_match_algorithm import EdgeMatchingAlgorithm
from puzzle_solver.edge_matcher.composite_edge_matcher import CompositeEdgeMatcher
from puzzle_solver.solver.backtracking.solver import Solver
from test.solver.assert_puzzle_solved import assert_puzzle_solved
from puzzle_solver.test_data.generator.generator import Generator
from puzzle_solver.file_parser import get_sample_1
from puzzle_solver.model import Puzzle, PuzzlePiece


class TestBacktrackingSolver(unittest.TestCase):
    def test_backtracking_solver_on_test_data(self):
        random.seed(1337)
        dim_x, dim_y = 5, 5
        puzzle = Generator(dim_x, dim_y).generate()
        solved_puzzle = self.solve(puzzle)
        assert_puzzle_solved(solved_puzzle, dim_x, dim_y)

    def test_backtracking_solver_on_sample(self):
        puzzle = get_sample_1()
        # todo solved_puzzle = self.solve(puzzle)

    def solve(self, puzzle: Puzzle) -> list[list[PuzzlePiece]]:
        normalized_puzzle = puzzle.get_normalize()
        edge_matcher = CompositeEdgeMatcher(
            [EdgeMatchingAlgorithm.MOCK], normalized_puzzle
        )
        frame_matrix, inner_matrix = create_edge_match_matrices(
            edge_matcher.match, normalized_puzzle
        )
        piece_matcher_frame = PieceMatcher(frame_matrix, puzzle)
        piece_matcher_inner = PieceMatcher(inner_matrix, puzzle)
        straight_edge = piece_matcher_frame.get_straight_edge()
        solver = Solver(
            piece_matcher_frame, piece_matcher_inner, normalized_puzzle, straight_edge
        )
        return solver.solve()
