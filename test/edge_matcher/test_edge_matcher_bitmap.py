import unittest

from puzzle_solver.edge_matcher.bitmap.edge_matcher import BitmapEdgeMatcher
from puzzle_solver.model import Edge, Point, Puzzle


def create_edge(coords, id_: str) -> Edge:
    points = [Point(x, y) for (x, y) in coords]
    return Edge(points, id_, piece_id="p11")


def check_similarity(
    testcase: unittest.TestCase, edge1: Edge, edge2: Edge, expected_similarity: float
):
    similarity = BitmapEdgeMatcher().match_masks(edge1, edge2)
    testcase.assertAlmostEqual(similarity, expected_similarity, delta=0.02)


class TestBitmapEdgeMatcher(unittest.TestCase):
    def test_various_edges(self):
        test_edges = [
            # Checks if 50% of the reconstructed edge surfaces overlap.
            (
                create_edge(
                    [(0, 0), (1, 0), (1, 1), (2, 1), (2, 0), (3, 0), (4, 0), (5, 0)],
                    id_="edge1",
                ),
                create_edge(
                    [(0, 0), (1, 0), (1, 1), (2, 1), (3, 1), (3, 0), (4, 0), (5, 0)],
                    id_="edge2",
                ),
                0.50,
            ),
            # Checks if 25% of the reconstructed edge surfaces overlap.
            (
                create_edge(
                    [(0, 0), (0, 1), (1, 1), (2, 1), (3, 1), (3, 0), (4, 0), (5, 0)],
                    id_="edge1",
                ),
                create_edge(
                    [(0, 0), (1, 0), (2, 0), (2, 1), (3, 1), (4, 1), (4, 0), (5, 0)],
                    id_="edge2",
                ),
                0.25,
            ),
            # Checks if 100% of the reconstructed edge surfaces overlap, while the edge3 is a mirrored version of edge1.
            (
                create_edge(
                    [(0, 0), (1, 0), (1, 1), (2, 1), (2, 0), (3, 0)], id_="edge1"
                ),
                create_edge(
                    [(0, 1), (1, 1), (1, 0), (2, 0), (2, 1), (3, 1)], id_="edge3"
                ),  # edge1 rotated
                1.0,
            ),
            # Checks if 100% of the reconstructed edge surfaces overlap. Both edges are the same.
            (
                create_edge(
                    [(0, 0), (1, 0), (1, 1), (2, 1), (2, 0), (3, 0)], id_="edge1"
                ),
                create_edge(
                    [(0, 0), (1, 0), (1, 1), (2, 1), (2, 0), (3, 0)], id_="edge1"
                ),
                1.0,
            ),
        ]

        for edge1, edge2, expected_similarity in test_edges:
            with self.subTest(
                edge1=edge1, edge2=edge2, expected_similarity=expected_similarity
            ):
                check_similarity(self, edge1, edge2, expected_similarity)


if __name__ == "__main__":
    unittest.main()
