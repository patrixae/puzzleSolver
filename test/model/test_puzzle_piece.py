import unittest
from puzzle_solver.model import PuzzlePiece
from puzzle_solver.test_data.generator.edge_generator import generate_edge


class TestPuzzlePiece(unittest.TestCase):

    def test_rotation(self):
        edges = [generate_edge(1, str(i)) for i in range(4)]
        piece = PuzzlePiece(edges=edges, id="piece1", vertices=[])
        assert piece.get_edge_ids() == ["0", "1", "2", "3"]
        piece.rotate_n_times(1)
        assert piece.get_edge_ids() == ["3", "0", "1", "2"]
