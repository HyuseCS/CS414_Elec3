# =============================================================================
# CS 414 - 4B | Activity 1 (Part 2): Havel-Hakimi Algorithm
# Problem No. 5
# Degree Sequence: S5 = (5, 4, 3, 2, 1, 3)
#
# Group Members:
#   Wency Casiño        Ken Charles Besa      Birky Pacuribot
#   Kerby Fabria        Carl Rejas            Cj Legaspi
#   Charles Sorongon
# =============================================================================

import networkx as nx

from visualization import (
    draw_graph,
    draw_steps,
    show_steps_interactive,
    keep_windows_open,
)

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
def is_graphical(sequence):
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
    G = nx.Graph()                      #Graph Builder
    G.add_nodes_from(node_labels)

    # Pair each node label with its target degree: [(degree, label), ...]
    indexed = list(zip(sequence, node_labels))
    history = []

    while True:
        # Sort pairs by degree, highest first
        indexed = sorted(indexed, key=lambda x: x[0], reverse=True)

        # Drop nodes whose degree requirement is already satisfied
        indexed = [(d, v) for d, v in indexed if d > 0]

        # Stop when no unsatisfied degrees remain
        if not indexed:
            break

        d, v = indexed[0]  # Node with the highest remaining degree
        neighbors = []

        # Connect v to the next d highest-degree nodes, then remove v
        for i in range(1, d + 1):
            neighbor_deg, neighbor = indexed[i]
            G.add_edge(v, neighbor)
            indexed[i] = (neighbor_deg - 1, neighbor)  # Reduce neighbor's remaining degree
            neighbors.append(neighbor)

        indexed = indexed[1:]  # Remove v — its degree is now fully satisfied

        history.append({
            "vertex":    v,
            "degree":    d,
            "neighbors": neighbors,
            "remaining": {label: deg for deg, label in indexed},
        })

    return G, history


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


def read_sequence(): # Input validation and Normalization
    """
    Reads a degree sequence typed by the user, re-prompting until it is valid.

    Accepts numbers separated by spaces or commas. A blank line falls back to
    S5 from the activity, so the graded run needs no typing.

    Returns:
        list of non-negative integers, or None if input ends (Ctrl-D)
    """
    while True:
        try:
            raw = input("  Enter degree sequence (blank = S5 -> 5, 4, 3, 2, 1, 3): ").strip()
        except EOFError:
            return None

        if not raw:
            return [5, 4, 3, 2, 1, 3]

        try:
            sequence = [int(token) for token in raw.replace(",", " ").split()]
        except ValueError:
            print("  Invalid input: use whole numbers only, e.g. 5 4 3 2 1 3\n")
            continue

        if not sequence:
            print("  Invalid input: the sequence is empty.\n")
            continue
        if any(d < 0 for d in sequence):
            print("  Invalid input: a degree cannot be negative.\n")
            continue

        return sequence


def ask_next_action():
    """
    Asks whether to analyse another sequence or quit.

    Returns:
        True to run again, False to exit
    """
    while True:
        print("\n" + "-" * 60)
        print("  [1] Enter another sequence")
        print("  [2] Exit")
        try:
            choice = input("  Choose: ").strip()
        except EOFError:
            return False

        if choice == "1":
            print()
            return True
        if choice in ("2", ""):
            return False
        print("  Please enter 1 or 2.")


def main():
    """
    Entry point. Loops over user-supplied degree sequences. For each one:
      a. Havel-Hakimi graphicality check (with step-by-step console output)
      b. Graph construction + edge list + degree verification
      c. Visual plot via matplotlib (detached window)
    """
    print("=" * 60)
    print("  CS 414-4B | Activity 1 | Problem 5")
    print("=" * 60)

    while True:
        sequence = read_sequence()
        if sequence is None:
            break

        node_labels = [f"v{i + 1}" for i in range(len(sequence))]

        print(f"\n  Input sequence: {sequence}")
        print(f"  Number of vertices (n) = {len(sequence)}")
        print(f"  Sum of degrees = {sum(sequence)}")
        print("=" * 60)

        # ── Part a: Check graphicality ─────────────────────────────
        print("\n[ Part a ] Havel-Hakimi Reduction Steps\n")
        graphical = is_graphical(list(sequence))

        if graphical:
            print("\n  Result: The sequence IS graphical. A simple graph exists.")

            # ── Part b: Build graph and report ─────────────────────
            print("\n" + "=" * 60)
            print("[ Part b ] Graph Construction & Verification\n")
            G, history = build_graph(list(sequence), node_labels)
            print_results(G, node_labels)

            # ── Part c: Visualise ──────────────────────────────────
            print("\n" + "=" * 60)
            print("[ Part c ] Rendering Graph Plot\n")
            draw_graph(G, sequence, node_labels)
            draw_steps(G, history, sequence)
            show_steps_interactive(G, history, sequence)
        else:
            print("\n  Result: The sequence is NOT graphical.")
            print("  The network CANNOT be constructed with this degree sequence.")

        if not ask_next_action():
            break

    print("\n  Done. Close the plot window(s) to finish.")
    keep_windows_open()   # blocks so the detached windows stay on screen


if __name__ == "__main__":
    main()