import unittest
from typing import Dict, List

import pandas as pd
from plotly.graph_objs import Figure

from eval.eval_ground_truth import GroundTruth
from eval.util import save_plotly
from puzzle_solver.edge_matcher.composite_edge_matcher import instantiate
from puzzle_solver.edge_matcher.edge_match_algorithm import EdgeMatchingAlgorithm
from puzzle_solver.edge_matcher.edge_match_matrix import (
    create_edge_match_matrix,
    EdgeMatchMatrix,
)
import plotly.graph_objects as go

from puzzle_solver.model import Puzzle
from puzzle_solver.file_parser import get_puzzle_104


class EdgeMatchAlgoEval:
    def __init__(self, puzzle: Puzzle, edge_match_algorithms: List[EdgeMatchingAlgorithm]):
        self.gt: GroundTruth = GroundTruth(puzzle=puzzle)
        self.edge_match_algorithms: List[EdgeMatchingAlgorithm] = edge_match_algorithms
        self.puzzle: Puzzle = puzzle
        self.emms: Dict[str, EdgeMatchMatrix] = self.get_emms()

    def get_df_from_emm(self, emm: EdgeMatchMatrix) -> pd.DataFrame:
        name_by_index = {v: k for k, v in emm.index_by_id.items()}
        df = pd.DataFrame(emm.matrix)
        df.index = [name_by_index[i] for i in df.index]
        df.columns = [name_by_index[i] for i in df.columns]
        return df

    def get_emms(self) -> Dict[str, EdgeMatchMatrix]:
        emms: Dict[str, EdgeMatchMatrix] = {}
        for edge_match_algorithm in self.edge_match_algorithms:
            edge_matcher = instantiate(alg=edge_match_algorithm, puzzle=self.puzzle)
            emm: EdgeMatchMatrix = create_edge_match_matrix(edge_matcher=edge_matcher.match, puzzle=self.puzzle,
                                                            name=edge_match_algorithm.name)
            emms[edge_match_algorithm.value] = emm
        return emms

    def calculate_overall_accuracy(self, emm: EdgeMatchMatrix) -> Dict[str, float]:
        df = self.get_df_from_emm(emm=emm)
        gt_edges = self.gt.fit_edges
        outer_edges = self.gt.outer_edges_amount

        counts = {1: 0, 2: 0, 3: 0, 5: 0, 10: 0, 11: 0, 12:0, 13:0, 14:0, 20:0}
        total_rows = len(df) - outer_edges

        for k in counts.keys():
            print(f"accuraccy: {k}")
            for row_label, row in df.iterrows():
                sorted_indices = row.sort_values(ascending=False).index.tolist()
                correct_match = gt_edges.get(row_label)

                if correct_match in sorted_indices[:k]:
                    counts[k] += 1
                elif correct_match is not None:
                    print(f"edge {row_label} should be matched with: {correct_match} correct match at nr: {sorted_indices.index(correct_match)}")

        return {
            "top1_count": counts[1],
            "top5_count": counts[5],
            "top10_count": counts[10],
            "total_rows": total_rows,
            "percent_in_top1": round((counts[1] / total_rows) * 100, 2),
            "percent_in_top2": round((counts[2] / total_rows) * 100, 2),
            "percent_in_top3": round((counts[3] / total_rows) * 100, 2),
            "percent_in_top5": round((counts[5] / total_rows) * 100, 2),
            "percent_in_top10": round((counts[10] / total_rows) * 100, 2)
        }

    def plot_interactive_histogram(self, edge_match_matrix: EdgeMatchMatrix, show_fig: bool = False):
        """
        Plots an interactive histogram for each row of the given DataFrame using Plotly.
        Dropdown allows selection of rows. Bars are annotated and have custom hover info.
        """
        df = self.get_df_from_emm(emm=edge_match_matrix)
        data = []
        row_names = []
        for idx, row in df.iterrows():
            sorted_row = row.sort_values(ascending=False)
            row_names.append(idx)
            data.append((sorted_row.index.tolist(), sorted_row.values.tolist()))

        fig: Figure = go.Figure()

        for i, (columns, values) in enumerate(data):
            row_name = row_names[i]
            edge_to_highlight = self.gt.fit_edges.get(row_name)

            # Assign color: red if column matches the highlight, blue otherwise
            colors = ["red" if col == edge_to_highlight else "blue" for col in columns]

            fig.add_trace(
                go.Bar(
                    x=columns,
                    y=values,
                    visible=(i == 0),
                    name=row_name,
                    marker=dict(color=colors),
                    hovertemplate="EdgeID: %{x}<br>Similarity: %{y:.2f}<extra></extra>",
                )
            )

        # Precompute annotation sets for each row
        annotations_by_row = []
        for _, (columns, values) in enumerate(data):
            annotations = []
            for j, (x, y) in enumerate(zip(columns, values)):
                annotations.append(
                    dict(
                        x=j,
                        y=y + 0.02 if j % 2 == 0 else y - 0.02,
                        text=f"{y:.2f}",
                        showarrow=False,
                        font=dict(size=10),
                        yanchor="bottom" if j % 2 == 0 else "top",
                    )
                )
            annotations_by_row.append(annotations)

        # Create dropdown buttons
        dropdown_buttons = []
        for i, name in enumerate(row_names):
            visible = [j == i for j in range(len(row_names))]

            dropdown_buttons.append(
                dict(
                    label=name,
                    method="update",
                    args=[
                        {"visible": visible},
                        {
                            "annotations": annotations_by_row[i],
                            "title": f"Histogram for {name}",
                        },
                    ],
                )
            )

        # Final layout update
        fig.update_layout(
            updatemenus=[
                dict(
                    active=0,
                    buttons=dropdown_buttons,
                    x=0.5,
                    xanchor="center",
                    y=1.15,
                    yanchor="top",
                )
            ],
            title=f"Histogram for {edge_match_matrix.name}",
            xaxis_title="EdgeID",
            yaxis_title="Similarity",
            height=500,
            margin=dict(t=100),
            annotations=annotations_by_row[0],
        )

        save_plotly(fig=fig, filename=edge_match_matrix.name)
        if show_fig:
            fig.show()


class TestEvaluateMatchers(unittest.TestCase):
    def test_evaluate_bitmap_image_and_euclidean_on_puzzle_104(self):
        puzzle = get_puzzle_104().get_normalize()
        edge_match_algorithms: List[EdgeMatchingAlgorithm] = [
            EdgeMatchingAlgorithm.BITMAP_IMAGE,
            EdgeMatchingAlgorithm.EUCLIDEAN
        ]
        edge_eval: EdgeMatchAlgoEval = EdgeMatchAlgoEval(
            puzzle=puzzle, edge_match_algorithms=edge_match_algorithms
        )

        expected_results = {
            EdgeMatchingAlgorithm.EUCLIDEAN.value: {'top1_count': 315, 'top5_count': 372, 'top10_count': 374,
                                                       'total_rows': 374, 'percent_in_top1': 84.22,
                                                       'percent_in_top2': 94.92,
                                                       'percent_in_top3': 98.4,
                                                       'percent_in_top5': 99.47, 'percent_in_top10': 100.0},
            EdgeMatchingAlgorithm.BITMAP_IMAGE.value: {'top1_count': 334, 'top5_count': 373, 'top10_count': 374,
                                                     'total_rows': 374, 'percent_in_top1': 89.3,
                                                     'percent_in_top2': 96.52,
                                                     'percent_in_top3': 99.2, 'percent_in_top5': 99.73,
                                                     'percent_in_top10': 100.0}}
        for emm_name in edge_eval.emms:
            emm = edge_eval.emms[emm_name]
            edge_eval.plot_interactive_histogram(emm)
            actual_result = edge_eval.calculate_overall_accuracy(emm)
            print(emm_name, actual_result)
            assert actual_result == expected_results[emm_name]
