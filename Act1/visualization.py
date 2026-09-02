# =============================================================================
# CS 414 - 4B | Activity 1 (Part 2): Havel-Hakimi Algorithm
# Visualization module
#
# All matplotlib drawing lives here so that problem5_havel_hakimi.py holds
# only the algorithm itself. Import what you need:
#
#   from visualization import draw_graph, draw_steps, show_steps_interactive
# =============================================================================

from pathlib import Path

import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.widgets import Button

# Save images next to this file, not in whatever directory the script was run from
OUTPUT_DIR = Path(__file__).resolve().parent


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

    # Use a circular layout so that all nodes are evenly spaced
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
        f"Degree Sequence = {tuple(sequence)}\n"
        "Havel-Hakimi Graph (CS 414-4B Group 5)",
        fontsize=12, fontweight='bold', pad=15
    )
    plt.margins(0.15)  # room for the deg= labels drawn outside the nodes
    plt.axis('off')
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "problem5_graph.png", dpi=150)
    plt.show(block=False)   # detached: the window stays open, the script continues
    plt.pause(0.1)          # gives the window a moment to draw
    print("\n  Graph saved as 'problem5_graph.png'")


def draw_panel(ax, G, pos, outer, history, index, title_size=10):
    """
    Draws a single frame of the construction onto one axes.

    Parameters:
        ax      : the matplotlib axes to draw on
        G       : the finished NetworkX graph
        pos     : node positions, shared by every frame
        outer   : slightly pushed-out positions for the small side labels
        history : step records returned by build_graph()
        index   : which step to show; index == len(history) draws the final graph
    """
    ax.clear()

    # Edges contributed by every step before this one
    drawn = [(record["vertex"], neighbor)
             for record in history[:index]
             for neighbor in record["neighbors"]]

    if index < len(history):
        step = history[index]
        active = step["vertex"]
        remaining = step["remaining"]
        new_edges = [(active, neighbor) for neighbor in step["neighbors"]]

        # Orange = the vertex being taken, blue = still needs edges, grey = done
        colors = ['#E8743B' if node == active
                  else '#4A90D9' if remaining.get(node, 0) > 0
                  else '#C9CDD2'
                  for node in G.nodes()]
        side_labels = {node: f"needs {remaining.get(node, 0)}" for node in G.nodes()}
        title = (f"Step {index + 1}: take {active} (degree {step['degree']})\n"
                 f"connect to {', '.join(step['neighbors'])}")
    else:
        new_edges = []
        colors = ['#4A90D9'] * G.number_of_nodes()
        side_labels = {node: f"deg={G.degree(node)}" for node in G.nodes()}
        title = "Final graph\nall degree requirements satisfied"

    nx.draw_networkx_edges(G, pos, edgelist=drawn, ax=ax,
                           edge_color='#888888' if index == len(history) else '#C4C4C4',
                           width=2 if index == len(history) else 1.5)
    nx.draw_networkx_edges(G, pos, edgelist=new_edges, ax=ax,
                           edge_color='#E8743B', width=2.8)
    nx.draw_networkx_nodes(G, pos, ax=ax, node_color=colors, node_size=950)
    nx.draw_networkx_labels(G, pos, ax=ax, font_size=10,
                            font_color='white', font_weight='bold')
    nx.draw_networkx_labels(G, outer, ax=ax, font_size=7.5,
                            font_color='#333333', labels=side_labels)

    ax.set_title(title, fontsize=title_size, fontweight='bold')
    ax.margins(0.24)
    ax.axis('off')


def draw_steps(G, history, sequence):
    """
    Saves one image holding every step of the construction side by side, so the
    build-up can be pasted into the write-up. The window itself is closed again;
    show_steps_interactive() is what stays on screen.

    Parameters:
        G        : the finished NetworkX graph
        history  : step records returned by build_graph()
        sequence : original degree sequence (for the figure title)
    """
    pos = nx.circular_layout(G)
    outer = {node: (x * 1.28, y * 1.28) for node, (x, y) in pos.items()}

    panels = len(history) + 1              # one per step, plus the final graph
    cols = 2
    rows = -(-panels // cols)              # ceiling division
    fig, axes = plt.subplots(rows, cols, figsize=(5.4 * cols, 4.6 * rows))
    axes = list(axes.flat)

    for i in range(panels):
        draw_panel(axes[i], G, pos, outer, history, i)

    # Blank out any unused panel in the grid
    for ax in axes[panels:]:
        ax.axis('off')

    fig.suptitle(f"Havel-Hakimi construction, step by step — {tuple(sequence)}",
                 fontsize=13, fontweight='bold')
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "problem5_steps.png", dpi=150)
    plt.close(fig)          # keep the screen clear; the stepper below is the live view
    print("  Step-by-step figure saved as 'problem5_steps.png'")


def show_steps_interactive(G, history, sequence):
    """
    Opens a window showing one step at a time, with Prev and Next buttons so the
    construction can be walked through at the reader's own pace.

    Parameters:
        G        : the finished NetworkX graph
        history  : step records returned by build_graph()
        sequence : original degree sequence (for the window title)
    """
    pos = nx.circular_layout(G)
    outer = {node: (x * 1.28, y * 1.28) for node, (x, y) in pos.items()}
    last = len(history)                    # index of the final-graph frame

    fig = plt.figure(figsize=(7.2, 6.6))
    fig.suptitle(f"Havel-Hakimi construction — {tuple(sequence)}",
                 fontsize=13, fontweight='bold')
    ax = fig.add_axes([0.04, 0.15, 0.92, 0.74])
    counter = fig.text(0.5, 0.085, "", ha='center', fontsize=9, color='#555555')

    current = {"index": 0}

    def render():
        draw_panel(ax, G, pos, outer, history, current["index"], title_size=11)
        counter.set_text(f"frame {current['index'] + 1} of {last + 1}"
                         "   —   use the buttons below")
        fig.canvas.draw_idle()

    def move(delta):
        def on_click(event):
            current["index"] = max(0, min(last, current["index"] + delta))
            render()
        return on_click

    button_prev = Button(fig.add_axes([0.32, 0.02, 0.15, 0.055]), "< Prev")
    button_next = Button(fig.add_axes([0.53, 0.02, 0.15, 0.055]), "Next >")
    button_prev.on_clicked(move(-1))
    button_next.on_clicked(move(1))

    # Matplotlib drops widgets that nothing references, so keep them on the figure
    fig.step_buttons = (button_prev, button_next)

    render()
    plt.show(block=False)
    plt.pause(0.1)
    print("  Interactive stepper open — click '< Prev' and 'Next >' to walk the steps.")


def keep_windows_open():
    """
    Blocks until the user closes the plot windows. Call this once, at the very
    end, so the detached figures stay on screen after the script finishes.
    """
    plt.show()
