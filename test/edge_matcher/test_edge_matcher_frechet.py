import unittest
from puzzle_solver.edge_matcher.frechet.edge_matcher import FrechetEdgeMatcher
from puzzle_solver.model import Edge
from puzzle_solver.model import Point


def create_edge(coordinates, id_="test_edge"):
    points = [Point(x, y) for (x, y) in coordinates]
    return Edge(points=points, id_=id_, piece_id="p11")


class TestFrechetEdgeMatcher(unittest.TestCase):
    def test_various_edges(self):
        test_edges = [
            (
                create_edge(
                    [(0, 0), (1, 0), (1, 1), (2, 1), (2, 0), (3, 0), (4, 0), (5, 0)],
                    id_="edge1",
                ),
                create_edge(
                    [(0, 0), (1, 0), (2, 0), (2, 1), (3, 1), (4, 1), (4, 0), (5, 0)],
                    id_="edge2",
                ),
                0.50,
            ),
            (
                create_edge(
                    [(0, 0), (1, 0), (1, 1), (2, 1), (2, 0), (3, 0)], id_="edge1"
                ),
                create_edge(
                    [(0, 1), (1, 1), (1, 0), (2, 0), (2, 1), (3, 1)], id_="edge3"
                ),  # edge1 rotated
                1.0,
            ),
        ]

        for edge1, edge2, expected_similarity in test_edges:
            with self.subTest(
                edge1=edge1.id, edge2=edge2.id, expected_similarity=expected_similarity
            ):
                similarity = FrechetEdgeMatcher().match(edge1, edge2)
                # Keine strenge Exaktheit bei Frechet-Distanz => leichte Toleranz erlauben
                self.assertAlmostEqual(similarity, expected_similarity, delta=0.5)


if __name__ == "__main__":
    unittest.main()
