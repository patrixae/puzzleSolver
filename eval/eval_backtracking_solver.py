import random
import unittest
from eval.util import plot_tree
from puzzle_solver.edge_matcher.edge_match_matrix import create_edge_match_matrices
from puzzle_solver.piece_matcher.piece_matcher import PieceMatcher
from puzzle_solver.edge_matcher.edge_match_algorithm import EdgeMatchingAlgorithm
from puzzle_solver.solver.backtracking.solver import FrameSolver, InnerSolver
from puzzle_solver.edge_matcher.composite_edge_matcher import CompositeEdgeMatcher
from puzzle_solver.solver.puzzle_context import PuzzleContext
from puzzle_solver.test_data.generator.generator import Generator


class TestSolver(unittest.TestCase):
    def test_backtracking_solver(self):
        random.seed(1337)
        dim_x, dim_y = 5, 5
        puzzle = Generator(dim_x, dim_y).generate()
        normalized_puzzle = puzzle.get_normalize()
        edge_matcher = CompositeEdgeMatcher([EdgeMatchingAlgorithm.MOCK], puzzle)
        frame_matrix, inner_matrix = create_edge_match_matrices(
            edge_matcher.match, normalized_puzzle
        )
        piece_matcher_frame = PieceMatcher(frame_matrix, puzzle)
        piece_matcher_inner = PieceMatcher(inner_matrix, puzzle)

        ctx = PuzzleContext(len(puzzle))
        straight_edge = piece_matcher_frame.get_straight_edge()
        frame_solver = FrameSolver(piece_matcher_frame, puzzle, ctx, straight_edge)
        frame_solver.solve()
        plot_tree(frame_solver.root, "frame_solver_tree")
        inner_solver = InnerSolver(piece_matcher_inner, puzzle, ctx, straight_edge)
        inner_solver.solve()
        plot_tree(inner_solver.root, "inner_solver_tree")
