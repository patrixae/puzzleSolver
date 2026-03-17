import os
from typing import Any
import matplotlib.pyplot as plot
from matplotlib.figure import Figure as PltFigure
import networkx as nx

from plotly.graph_objs import Figure

from puzzle_solver.edge_matcher.edge_match_matrix import EdgeMatchMatrix
from puzzle_solver.model import PuzzlePiece
from puzzle_solver.piece_placer import PlacedPiece
from puzzle_solver.solver.backtracking.backtracking import Node


def save_plot(fig: PltFigure, filename: str, dpi: int = 100) -> None:
    base_dir = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(base_dir, f"../test_results/{filename}.png")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    fig.savefig(path, bbox_inches="tight", dpi=dpi)


def save_plotly(fig: Figure, filename: str) -> None: # type: ignore
    base_dir = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(base_dir, f"../test_results/{filename}.html")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    fig.write_html(path)
    print(f"File written: {path}")


def plot_placed_puzzle(
        placed_pieces: dict[str, PlacedPiece], pieces: list[PuzzlePiece], filename: str
) -> None:
    fig, ax = plot.subplots(figsize=(16, 12))

    for id, placed_piece in placed_pieces.items():
        piece = [x for x in pieces if x.id == id][0]
        middle_point = piece.get_middle_point()
        x_shift = placed_piece.x - middle_point.x
        y_shift = placed_piece.y - middle_point.y
        x_list = []
        y_list = []
        for edge in piece.edges:
            edge.rotate_points(middle_point, placed_piece.angle)
            x, y = zip(*edge.get_edge_coordinates())
            x_list.extend([i + x_shift for i in x])
            y_list.extend([i + y_shift for i in y])
        ax.scatter(x_list, y_list, s=5)
        ax.text(middle_point.x + x_shift, middle_point.y + y_shift, piece.id)
    # ax.invert_yaxis()
    ax.grid(True)
    ax.set_aspect("equal", adjustable="box")

    save_plot(fig, filename)
    plot.close(fig)


def plot_edge_match_heat_map(edge_match_matrix: EdgeMatchMatrix, file_name: str) -> None:
    fig, ax = plot.subplots()
    matrix: list[list[float]] = edge_match_matrix.matrix.tolist()  # type: ignore
    ax.imshow(matrix)

    # Show all ticks and label them with the respective list entries
    labels = [
        edge_match_matrix.meta_data_by_index[i].edge.id for i in range(len(matrix))
    ]
    ax.set_xticks(
        range(len(matrix)),
        labels=labels,
        rotation=90,
        ha="right",
        rotation_mode="anchor",
        fontsize=2,
    )
    ax.set_yticks(range(len(matrix)), labels=labels, fontsize=2)

    # Loop over data dimensions and create text annotations.
    for i, row in enumerate(matrix):
        for j, value in enumerate(row):
            ax.text(
                j,
                i,
                f".{round(float(value) * 10)}",
                ha="center",
                va="center",
                color="w",
                fontsize=1,
            )
    fig.tight_layout()
    save_plot(fig, f"heatmap-{file_name}", dpi=1000)


def plot_tree(root: Node, filename: str = "backtracking-tree-graph") -> None:
    def add_nodes_edges( #type: ignore
            graph: nx.DiGraph,
            node: Node | None,
            edge_labels: dict[tuple[str, str], str],
    )->None:
        if node is None:
            return
        node_label = f"{node.piece_id}-{node.depth}-{node.parent.piece_id if node.parent else "root"}"
        graph.add_node(node_label, probability=node.probability)
        for child in node.children:
            if child is not None:
                child_label = f"{child.piece_id}-{child.depth}-{node.piece_id}"
                graph.add_node(child_label, probability=child.probability)
                graph.add_edge(node_label, child_label)
                edge_labels[(node_label, child_label)] = f"{child.probability:.2f}"
                add_nodes_edges(graph, child, edge_labels)

    edge_labels: dict[tuple[str, str], str] = {}
    graph = nx.DiGraph()
    add_nodes_edges(graph, root, edge_labels)
    fig, ax = plot.subplots(figsize=(40, 32))
    pos: Any = nx.nx_agraph.graphviz_layout(
        graph, prog="dot", args="-Gnodesep=4 -Granksep=4"
    )
    nx.draw(
        graph,
        pos,
        with_labels=True,
        node_color="lightblue",
        edge_color="gray",
        arrows=True,
        ax=ax,
    )
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, ax=ax)
    plot.title("Backtracking tree")
    save_plot(fig, filename, 300)
    plot.close(fig)
