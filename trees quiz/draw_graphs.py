from pathlib import Path

import matplotlib.pyplot as plt
import networkx as nx

OUTPUT_DIR = Path(__file__).resolve().parent

GRAPHS = {
    "number1": (
        {"A": (0, 0), "B": (2, 0), "a1": (0, 1), "a2": (-1, 0), "a3": (0, -1),
         "b1": (2, 1), "b2": (3, 0), "b3": (2, -1)},
        [("A", "B"), ("A", "a1"), ("A", "a2"), ("A", "a3"),
         ("B", "b1"), ("B", "b2"), ("B", "b3")],
    ),
    "number2": (
        {"A": (0, 0), "B": (2, 0), "C": (4, 0), "a1": (-1, 0.8), "a2": (-1, -0.8),
         "b1": (2, -1), "c1": (5, 0.8), "c2": (5, -0.8)},
        [("A", "B"), ("B", "C"), ("A", "a1"), ("A", "a2"),
         ("B", "b1"), ("C", "c1"), ("C", "c2")],
    ),
    "number4": (
        {"u": (0, 3), "v": (4, 3), "w": (0.5, 2), "x": (3, 2), "y": (2, 1), "z": (2.3, 0)},
        [("u", "v", 6), ("v", "z", 5), ("z", "y", 4), ("y", "x", 5), ("x", "w", 7)],
    ),
    "number5": (
        {"a": (0, 2), "c": (2, 2), "b": (0, 0), "d": (2, 0), "e": (3.5, 1),
         "f": (5, 1), "g": (6.5, 2), "i": (8, 2), "h": (6.5, 0)},
        [("a", "c"), ("a", "b"), ("a", "d"), ("c", "d"), ("b", "d"), ("c", "e"),
         ("d", "e"), ("e", "f"), ("f", "g"), ("g", "i"), ("f", "h")],
    ),
}

for name, (pos, edges) in GRAPHS.items():
    G = nx.Graph()
    G.add_nodes_from(pos)
    for u, v, *w in edges:
        G.add_edge(u, v, **({"weight": w[0]} if w else {}))
    plt.figure(figsize=(6, 4))
    nx.draw(G, pos, with_labels=True, node_color="#a6cee3", node_size=700,
            edgecolors="black", font_weight="bold")
    weights = nx.get_edge_attributes(G, "weight")
    if weights:
        nx.draw_networkx_edge_labels(G, pos, edge_labels=weights, font_size=12)
    plt.axis("equal")
    plt.savefig(OUTPUT_DIR / f"{name}.png", dpi=150, bbox_inches="tight")
    plt.close()
