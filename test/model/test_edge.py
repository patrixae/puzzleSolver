import unittest

from puzzle_solver.model.edge import Edge
from puzzle_solver.model.point import Point


class TestEdge(unittest.TestCase):

    def test_interpolating_point_count_short_edge_segment(self):
        points1 = [
            Point(0, 0),
            Point(2, 0),
            Point(4, 0),
            Point(6, 0),
        ]  # point count of 4
        points2 = [
            Point(0, 0),
            Point(3, 0),
            Point(4, 0),
            Point(10, 0),
        ]  # point count of 11
        edges = [
            Edge(points1, "t1", piece_id="p11"),
            Edge(points2, "t2", piece_id="p11"),
        ]
        expected = 3
        result = Edge.get_interpolating_point_count(edges)
        self.assertEqual(result, expected)

    def test_interpolate_edge_with_point_count(self):
        points = [Point(0, 0), Point(5, 0), Point(10, 0)]
        count = 21
        edge = Edge(points, "t1", piece_id="p11")
        dist_between = 0.5
        result = edge.get_edge_with_point_count(count)
        interp_points = result.get_points()
        self.assertEqual(len(interp_points), count)
        self.assertEqual(interp_points[0].get_length_to(interp_points[1]), dist_between)
