"""CS 414 Activity 1 Part 2 - Havel-Hakimi algorithm.

Checks each degree sequence from Part 1, builds the graph if it is
graphical, and plots it.
"""

import networkx as nx
import matplotlib.pyplot as plt

SEQUENCES = {
    "S1 (6 servers)":       [5, 4, 3, 2, 1, 1],
    "S2 (6 sensor nodes)":  [5, 4, 3, 2, 1, 0],
    "S3 (network switches)": [4, 3, 2, 2, 1, 0],
    "S4 (6 hex regions)":   [6, 3, 3, 2, 1, 1],
    "S5 (6 club members)":  [5, 4, 3, 2, 1, 3],
}


def havel_hakimi(seq):
    """Return (is_graphical, steps, reason). Prints nothing."""
    steps = []
    work = sorted(seq, reverse=True)
    if sum(work) % 2 != 0:
        return False, steps, f"sum of degrees {sum(work)} is odd"
    if any(d < 0 for d in work) or any(d > len(work) - 1 for d in work):
        return False, steps, f"a degree exceeds n-1 = {len(work) - 1} (or is negative)"

    while True:
        work = sorted(work, reverse=True)
        steps.append(list(work))
        if all(d == 0 for d in work):
            return True, steps, "all degrees reduced to zero"
        d = work[0]
        rest = work[1:]
        if d > len(rest):
            return False, steps, f"need to connect to {d} vertices but only {len(rest)} remain"
        for i in range(d):
            rest[i] -= 1
        if any(x < 0 for x in rest):
            return False, steps, "a degree became negative after subtraction"
        work = rest


def build_graph(seq):
    """Build a simple graph with exactly this degree sequence (Havel-Hakimi construction)."""
    g = nx.Graph()
    nodes = [f"v{i + 1}" for i in range(len(seq))]
    g.add_nodes_from(nodes)
    remaining = list(zip(seq, nodes))
    while True:
        remaining.sort(reverse=True)
        d, v = remaining[0]
        if d == 0:
            return g
        remaining[0] = (0, v)
        for i in range(1, d + 1):
            di, vi = remaining[i]
            g.add_edge(v, vi)
            remaining[i] = (di - 1, vi)


def run(name, seq):
    print("=" * 60)
    print(f"{name}: {seq}")
    ok, steps, reason = havel_hakimi(seq)
    for i, s in enumerate(steps):
        print(f"  step {i}: {s}")
    if not ok:
        print(f"  RESULT: NOT graphical - {reason}.")
        print("  The network cannot be built: no simple graph has these connection counts.")
        return
    print(f"  RESULT: GRAPHICAL - {reason}.")
    g = build_graph(seq)
    print(f"  edges: {sorted(tuple(sorted(e)) for e in g.edges())}")
    print("  verified degrees:")
    for v in sorted(g.nodes()):
        print(f"    {v}: {g.degree(v)}")
    assert sorted((d for _, d in g.degree()), reverse=True) == sorted(seq, reverse=True)

    plt.figure()
    pos = nx.spring_layout(g, seed=1)
    nx.draw(g, pos, with_labels=False, node_color="lightblue", node_size=900)
    nx.draw_networkx_labels(g, pos, {v: f"{v}\ndeg={g.degree(v)}" for v in g})
    plt.title(name)
    plt.savefig(f"{name.split()[0]}.png")
    print(f"  plot saved: {name.split()[0]}.png")


if __name__ == "__main__":
    for name, seq in SEQUENCES.items():
        run(name, seq)
    plt.show()
