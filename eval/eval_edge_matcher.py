import unittest
import matplotlib.pyplot as plot

from eval.util import save_plot
from puzzle_solver.edge_matcher.composite_edge_matcher import CompositeEdgeMatcher
from puzzle_solver.edge_matcher.edge_match_algorithm import EdgeMatchingAlgorithm
from puzzle_solver.edge_matcher.edge_match_matrix import (
    EdgeMatchMatrix,
    create_edge_match_matrix,
)
from puzzle_solver.model import Edge
from puzzle_solver.test_data import get_puzzle
from puzzle_solver.file_parser import get_sample_1


def plot_edge_match_matrix(edge_match_matrix: EdgeMatchMatrix, alg: str):
    fig, ax = plot.subplots(figsize=(16, 12))

    flattened_matrix = [i for sub in edge_match_matrix.matrix for i in sub]

    counts, _, bars = ax.hist(flattened_matrix, bins=10, edgecolor="black")
    ax.set_xlabel("Probability")
    ax.set_ylabel("Count")
    ax.set_title(f"Edge Matcher Eval: {alg}")
    for bar_, count in zip(bars, counts):
        ax.text(
            bar_.get_x() + bar_.get_width() / 2,
            count,
            count,
            ha="center",
            va="bottom",
            fontsize=9,
        )
    save_plot(fig, f"edge-match-matrix-{alg}-eval")
    plot.close(fig)


def visualise_edge_match(edge1: Edge, edge2: Edge) -> None:
    """
    Visualizes the comparison between two edges by plotting their point sets.
    :param edge1: The first edge to visualize.
    :param edge2: The second edge to visualize.
    :return:
    """
    x1, y1 = zip(*edge1.get_edge_coordinates())
    x2, y2 = zip(*edge2.get_edge_coordinates())

    plot.figure(figsize=(6, 6))
    plot.title(f"Comparison Edges {edge1.id} and {edge2.id}")
    plot.scatter(x1, y1, c="blue", label="Set 1")
    plot.scatter(x2, y2, c="red", label="Set 2")
    plot.legend()
    plot.gca().invert_yaxis()
    plot.grid(True)
    plot.savefig(f"ComparisonEdges{edge1.id}and{edge2.id}.png")


class TestEvalEdgeMatcher(unittest.TestCase):
    def test_mock_edge_matcher(self):
        puzzle = get_puzzle(9, 9, 42)
        edge_matcher = CompositeEdgeMatcher([EdgeMatchingAlgorithm.MOCK], puzzle)
        edge_match_matrix = create_edge_match_matrix(edge_matcher.match, puzzle)

        plot_edge_match_matrix(
            edge_match_matrix,
            "MOCK-Edge-Matcher",
        )

    def test_euclidean_edge_matcher(self):
        puzzle = get_sample_1().get_normalize()
        edge_matcher = CompositeEdgeMatcher([EdgeMatchingAlgorithm.EUCLIDEAN], puzzle)
        edge_match_matrix = create_edge_match_matrix(edge_matcher.match, puzzle)

        plot_edge_match_matrix(
            edge_match_matrix,
            "EUCLIDEAN-Edge-Matcher",
        )

    def test_sample_edge_distance(self):
        puzzle = get_sample_1().get_normalize()
        edge_matcher = CompositeEdgeMatcher(
            [EdgeMatchingAlgorithm.EDGEDISTANCE], puzzle
        )
        edge_match_matrix = create_edge_match_matrix(edge_matcher.match, puzzle)

        plot_edge_match_matrix(edge_match_matrix, "Sample-EdgeDistance")
