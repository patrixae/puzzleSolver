import unittest

from puzzle_solver.edge_matcher.composite_edge_matcher import (
    CompositeEdgeMatcher,
    EdgeMatchingAlgorithm,
)
from puzzle_solver.edge_matcher.edge_match_matrix import create_edge_match_matrix
from puzzle_solver.solver.gradient.gradient_solver import GradientSolver
from puzzle_solver.test_data.generator.generator import Generator
from test.solver.assert_puzzle_solved import assert_puzzle_solved


class TestGradientSolver(unittest.TestCase):

    def solve(self):
        dim_x, dim_y = 5, 5
        puzzle = Generator(dim_x, dim_y).generate()
        puzzle.shuffle(42)
        normalized_puzzle = puzzle.get_normalize()
        edge_matcher = CompositeEdgeMatcher([EdgeMatchingAlgorithm.MOCK], puzzle)
        matrix = create_edge_match_matrix(edge_matcher.match, normalized_puzzle)
        solved_puzzle = GradientSolver("test_results/test_gradient_solcer").solve(
            puzzle, matrix
        )
        assert_puzzle_solved(solved_puzzle, dim_x, dim_y)
