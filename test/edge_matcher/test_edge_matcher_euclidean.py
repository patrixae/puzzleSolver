import pytest
from puzzle_solver.model import Edge, Point
from puzzle_solver.model.edge import EdgeType
from puzzle_solver.edge_matcher.euclidean.edge_matcher import (
    EuclideanEdgeMatcher
)


class TestMaxPointDistanceEdgeMatcher:
    def setup_method(self) -> None:
        self.matcher = EuclideanEdgeMatcher()

        # Create points for our test edges
        male_points = [
            Point(0, 0),
            Point(1, 1),
            Point(2, 0),
            Point(3, 1),
            Point(4, 0),
            Point(5, 0),
        ]
        female_points = [
            Point(0, 0),
            Point(1, -1),
            Point(2, 0),
            Point(3, -1),
            Point(4, 0),
            Point(5, 0),
        ]

        # Create edges with appropriate IDs
        self.straight_edge = Edge([], "straight", piece_id="p11")
        self.male_edge = Edge(male_points, "male", piece_id="p11")
        self.female_edge = Edge(female_points, "female", piece_id="p11")

        # Ensure correct edge types
        self.straight_edge.type = EdgeType.OUTER
        self.male_edge.type = EdgeType.MALE
        self.female_edge.type = EdgeType.FEMALE

    def test_match_compatible_edges(self) -> None:
        # Male and female edges should match
        similarity = self.matcher.match(self.male_edge, self.female_edge)
        assert similarity > 0

        # Reverse match should also work
        similarity_reverse = self.matcher.match(self.female_edge, self.male_edge)
        assert similarity_reverse > 0

        # Should be symmetric
        assert similarity == pytest.approx(similarity_reverse)

    def test_match_incompatible_edges(self) -> None:
        # Same type edges shouldn't match
        assert self.matcher.match(self.male_edge, self.male_edge) == 0
        assert self.matcher.match(self.female_edge, self.female_edge) == 0

        # Outer edges shouldn't match with any edge
        assert self.matcher.match(self.straight_edge, self.male_edge) == 0
        assert self.matcher.match(self.straight_edge, self.female_edge) == 0

    def test_edge_distance_calculation(self) -> None:
        # Get prepared arrays for comparison
        male_pts, female_pts, compatible = self.matcher._prepare_edges_for_comparison(
            self.male_edge, self.female_edge
        )
        assert compatible
        
        distance = self.matcher._get_distance(male_pts, female_pts)
        # The maximum point distance should be positive
        assert distance["max_distance"] > 0
        assert distance["mean_distance"] > 0

        # Test with the same edge arrays
        distance_self = self.matcher._get_distance(male_pts, male_pts)
        assert distance_self["max_distance"] == 0
        assert distance_self["mean_distance"] == 0

    def test_edge_similarity_calculation(self)-> None:
        # For compatible edges - male and female
        similarity = self.matcher._calc_similarity_score(self.male_edge, self.female_edge)
        assert 0 < similarity <= 1.0         
        # Same result should be returned by the match method
        assert self.matcher.match(self.male_edge, self.female_edge) == pytest.approx(similarity)
        
        # The current implementation returns 0 for same type edges (no longer 1.0)
        assert self.matcher._calc_similarity_score(self.male_edge, self.male_edge) == 0

