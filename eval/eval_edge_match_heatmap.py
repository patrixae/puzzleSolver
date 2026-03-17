import os
import random
import unittest
from eval.util import plot_edge_match_heat_map
from puzzle_solver.edge_matcher.edge_match_matrix import (
    create_edge_match_matrix,
    create_edge_match_matrices,
)
from puzzle_solver.file_parser import get_sample_1
from puzzle_solver.edge_matcher.edge_match_algorithm import EdgeMatchingAlgorithm
from puzzle_solver.edge_matcher.composite_edge_matcher import CompositeEdgeMatcher
from puzzle_solver.test_data.test_data import get_puzzle


class TestEdgeMatchHeatMap(unittest.TestCase):
    def test_edge_match_heatmap_generator(self):
        dim_x, dim_y = 5, 5
        puzzle = get_puzzle(dim_x, dim_y, 42)
        normalized_puzzle = puzzle.get_normalize()
        edge_matcher = CompositeEdgeMatcher(
            [EdgeMatchingAlgorithm.MOCK], normalized_puzzle
        )
        frame_matrix, inner_matrix = create_edge_match_matrices(
            edge_matcher.match, normalized_puzzle
        )

        full_matrix = create_edge_match_matrix(edge_matcher.match, normalized_puzzle)

        plot_edge_match_heat_map(frame_matrix, "eval-frame")
        plot_edge_match_heat_map(inner_matrix, "eval-inner")
        plot_edge_match_heat_map(full_matrix, "eval-full")

    def test_edge_match_heatmap_sample(self):
        random.seed(1337)
        puzzle = get_sample_1()
        normalized_puzzle = puzzle.get_normalize()
        edge_matcher = CompositeEdgeMatcher(
            [EdgeMatchingAlgorithm.EDGEDISTANCE], normalized_puzzle
        )

        full_matrix = create_edge_match_matrix(edge_matcher.match, normalized_puzzle)

        plot_edge_match_heat_map(full_matrix, "eval-sample1-full")
