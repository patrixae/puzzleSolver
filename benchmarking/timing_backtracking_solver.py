import random
import pytest
from puzzle_solver.edge_matcher.edge_match_algorithm import EdgeMatchingAlgorithm
from puzzle_solver.edge_matcher.edge_match_matrix import create_edge_match_matrices
from puzzle_solver.model.edge import Edge
from puzzle_solver.model.puzzle import Puzzle
from puzzle_solver.piece_matcher.piece_matcher import PieceMatcher
from puzzle_solver.solver.backtracking.solver import FrameSolver
from puzzle_solver.edge_matcher.composite_edge_matcher import CompositeEdgeMatcher
from puzzle_solver.solver.puzzle_context import PuzzleContext
from puzzle_solver.test_data.generator.generator import Generator


def get_setup(seed: int, dim_x: int, dim_y: int) -> tuple[PieceMatcher, Puzzle, Edge]:
    random.seed(seed)
    puzzle = Generator(dim_x, dim_y).generate()
    normalized_puzzle = puzzle.get_normalize()
    edge_matcher = CompositeEdgeMatcher([EdgeMatchingAlgorithm.MOCK], puzzle)
    frame_matrix, _ = create_edge_match_matrices(edge_matcher.match, normalized_puzzle)
    piece_matcher_frame = PieceMatcher(frame_matrix, puzzle)
    straight_edge = piece_matcher_frame.get_straight_edge()
    return piece_matcher_frame, puzzle, straight_edge


CASES = [
    (1337, 5, 5),
    (42, 8, 8),
    (99, 10, 6),
    # (  73112, 10, 6),
    (871630, 15, 15),
]

IDS = [f"{s}-{w}x{h}" for s, w, h in CASES]


@pytest.mark.parametrize("seed,dim_x,dim_y", CASES, ids=IDS)
@pytest.mark.benchmark(group="frame_solver")
def test_frame_solver_performance(benchmark, seed, dim_x, dim_y):
    piece_matcher_frame, puzzle, straight_edge = get_setup(seed, dim_x, dim_y)

    def run_once():
        # fresh solver/ctx for each run
        ctx = PuzzleContext(len(puzzle))
        solver = FrameSolver(piece_matcher_frame, puzzle, ctx, straight_edge)
        return solver.solve()

    benchmark.group = f"frame_{dim_x}x{dim_y}"
    benchmark(run_once)
