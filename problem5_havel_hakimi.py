# =============================================================================
# CS 414 - 4B | Activity 1 (Part 2): Havel-Hakimi Algorithm
# Problem No. 5
# Degree Sequence: S5 = (5, 4, 3, 2, 1, 3)
#
# Group Members:
#   Wency Casiño        Ken Charles Besa      Birky Pacuribot
#   Kerby Fabria        Carl Rejas            Cj Legaspi
#   Charles Sorongon    Joseph Pendon
# =============================================================================

import networkx as nx
import matplotlib.pyplot as plt


def is_graphical(sequence):
    """
    Determines if a degree sequence is graphical using the Havel-Hakimi algorithm.

    The algorithm repeatedly:
      1. Sorts the sequence in non-increasing order.
      2. Removes the largest degree (d) from the front.
      3. Subtracts 1 from the next d elements.
      4. Repeats until all zeros (graphical) or a negative appears (not graphical).

    Returns True if graphical, False otherwise.
    Also prints each step of the reduction to the console.
    """
    seq = sorted(sequence, reverse=True)
    step = 1

    print(f"  Starting sequence (sorted): {seq}")

    while True:
        # Remove trailing zeros — they don't affect graphicality
        seq = [d for d in seq if d > 0]

        # Base case: all elements are zero → sequence is graphical
        if not seq:
            print(f"\n  All degrees reduced to zero.")
            return True

        # Fail: first degree exceeds the number of remaining vertices
        d = seq[0]
        remaining = len(seq) - 1
        if d > remaining:
            print(f"\n  Step {step}: Degree {d} > available nodes ({remaining}) → FAIL")
            return False

        print(f"\n  Step {step}: Sequence = {seq}")
        print(f"    Take largest degree: {d}")
        print(f"    Subtract 1 from next {d} elements: {seq[1:d+1]}")

        # Subtract 1 from the next d elements, keep the rest unchanged
        new_seq = [seq[i] - 1 for i in range(1, d + 1)] + seq[d + 1:]

        # Fail: subtraction produced a negative degree
        if any(x < 0 for x in new_seq):
            print(f"    Result has a negative value → FAIL")
            return False

        new_seq_sorted = sorted(new_seq, reverse=True)
        print(f"    Remaining (re-sorted): {new_seq_sorted}")
        seq = new_seq_sorted
        step += 1


def build_graph(sequence, node_labels):
    """
    Constructs a NetworkX graph from a graphical degree sequence using
    the Havel-Hakimi algorithm, tracking which nodes get connected at each step.

    Parameters:
        sequence   : list of integer degrees (e.g. [5, 4, 3, 2, 1, 3])
        node_labels: list of node names matching the degree sequence (e.g. ['v1',...,'v6'])

    Returns:
        G : a NetworkX Graph with the correct edges
    """
    G = nx.Graph()
    G.add_nodes_from(node_labels)

    # Pair each node label with its target degree: [(degree, label), ...]
    indexed = list(zip(sequence, node_labels))

    while True:
        # Sort pairs by degree, highest first
        indexed = sorted(indexed, key=lambda x: x[0], reverse=True)

        # Drop nodes whose degree requirement is already satisfied
        indexed = [(d, v) for d, v in indexed if d > 0]

        # Stop when no unsatisfied degrees remain
        if not indexed:
            break

        d, v = indexed[0]  # Node with the highest remaining degree

        # Connect v to the next d highest-degree nodes, then remove v
        for i in range(1, d + 1):
            neighbor_deg, neighbor = indexed[i]
            G.add_edge(v, neighbor)
            indexed[i] = (neighbor_deg - 1, neighbor)  # Reduce neighbor's remaining degree

        indexed = indexed[1:]  # Remove v — its degree is now fully satisfied

    return G


def print_results(G, node_labels):
    """
    Prints the edge list and the verified degree of every vertex to the console.

    Parameters:
        G          : the constructed NetworkX graph
        node_labels: list of node names (for ordered output)
    """
    print("\n  Edge list:")
    for u, v in sorted(G.edges()):
        print(f"    {u} — {v}")

    print("\n  Verified degree of each vertex:")
    for node in node_labels:
        print(f"    {node}: degree = {G.degree(node)}")


def draw_graph(G, sequence, node_labels):
    """
    Renders and saves a visual plot of the constructed graph using matplotlib.
    Nodes are labelled by their identifier and annotated with their degree.

    Parameters:
        G          : the constructed NetworkX graph
        sequence   : original degree sequence (for the title)
        node_labels: list of node names
    """
    plt.figure(figsize=(8, 6))

    # Use a circular layout so that all 6 nodes are evenly spaced
    pos = nx.circular_layout(G)

    # Draw edges first (behind nodes)
    nx.draw_networkx_edges(G, pos, edge_color='#888888', width=2)

    # Draw nodes
    nx.draw_networkx_nodes(G, pos, node_color='#4A90D9', node_size=1800)

    # Label each node with its name
    nx.draw_networkx_labels(G, pos, font_size=13, font_color='white', font_weight='bold')

    # Annotate each node with its degree, placed just outside the node
    degree_labels = {node: f"deg={G.degree(node)}" for node in G.nodes()}
    label_pos = {node: (x * 1.18, y * 1.18) for node, (x, y) in pos.items()}
    nx.draw_networkx_labels(G, label_pos, labels=degree_labels,
                            font_size=9, font_color='#222222')

    plt.title(
        f"Problem 5 — S5 = {tuple(sequence)}\n"
        "Havel-Hakimi Graph (CS 414-4B Group 5)",
        fontsize=12, fontweight='bold', pad=15
    )
    plt.axis('off')
    plt.tight_layout()
    plt.savefig("problem5_graph.png", dpi=150)
    plt.show()
    print("\n  Graph saved as 'problem5_graph.png'")


def main():
    """
    Entry point. Runs the full pipeline for Problem 5:
      a. Havel-Hakimi graphicality check (with step-by-step console output)
      b. Graph construction + edge list + degree verification
      c. Visual plot via matplotlib
    """
    sequence    = [5, 4, 3, 2, 1, 3]
    node_labels = ['v1', 'v2', 'v3', 'v4', 'v5', 'v6']

    print("=" * 60)
    print("  CS 414-4B | Activity 1 | Problem 5")
    print(f"  Input sequence S5: {sequence}")
    print("=" * 60)

    # ── Part a: Check graphicality ─────────────────────────────────
    print("\n[ Part a ] Havel-Hakimi Reduction Steps\n")
    graphical = is_graphical(list(sequence))

    if graphical:
        print("\n  Result: The sequence IS graphical. A simple graph exists.")
    else:
        print("\n  Result: The sequence is NOT graphical.")
        print("  The network CANNOT be constructed with this degree sequence.")
        return

    # ── Part b: Build graph and report ────────────────────────────
    print("\n" + "=" * 60)
    print("[ Part b ] Graph Construction & Verification\n")
    G = build_graph(list(sequence), node_labels)
    print_results(G, node_labels)

    # ── Part c: Visualise ─────────────────────────────────────────
    print("\n" + "=" * 60)
    print("[ Part c ] Rendering Graph Plot\n")
    draw_graph(G, sequence, node_labels)


if __name__ == "__main__":
    main()