import unittest
import random
import string

from eval.util import plot_tree
from puzzle_solver.solver.backtracking import backtracking
from puzzle_solver.piece_matcher import PieceMatchResult


def piece_matcher_get_next_piece(node: backtracking.Node) -> list[backtracking.Node]:
    def get_rand_result() -> PieceMatchResult:
        id_ = "".join(random.choices(string.ascii_uppercase + string.digits, k=5))
        return PieceMatchResult(id_, random.randint(0, 4), random.random())

    def get_node(res: PieceMatchResult, node: backtracking.Node) -> backtracking.Node:
        return backtracking.Node(node, node.depth + 1, res.id, res.probability, 0)

    return [get_node(get_rand_result(), node) for _ in range(3)]


class TestBacktracking(unittest.TestCase):
    def test_backtracking(self):
        pieces = 50  # How many pieces must be matched
        iterations = pieces**2
        root = backtracking.Node(None, 0, "root", 0, 0)
        root.children = piece_matcher_get_next_piece(root)

        # we wont need more than pieces**2 iterations
        for _ in range(iterations):
            best_node = backtracking.find_best(root)
            assert best_node
            if best_node.depth == (pieces - 1):  # reduce by one because we start at 0
                break
            best_node.children = piece_matcher_get_next_piece(best_node)

        else:
            # If we reach the else clause, the loop never broke
            self.fail(f"Failed to find a solution within {iterations} iterations")
        plot_tree(root)
