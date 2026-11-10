"""Replay of a finished Schelling segregation simulation."""

from typing import Any

import matplotlib.pyplot as plt
from matplotlib import colormaps
from matplotlib.animation import FuncAnimation
from matplotlib.colors import ListedColormap
from matplotlib.patches import Patch

from .model import EMPTY, SchellingModel

EMPTY_COLOR = "#f5f5f5"
# Hand-picked colors for small numbers of groups.
GROUP_COLORS = ("#e63946", "#1d3557", "#2a9d8f", "#f4a261", "#8338ec")
# Legend entries per column, so a long legend stays on the figure.
LEGEND_ROWS = 20


def group_colors(n_groups: int) -> list:
    """Return one distinct color per group, for any number of groups."""
    if n_groups <= len(GROUP_COLORS):
        return list(GROUP_COLORS[:n_groups])
    if n_groups <= 20:
        return list(colormaps["tab20"].colors[:n_groups])
    # Many groups: spread colors evenly over a continuous colormap.
    colormap = colormaps["turbo"]
    return [colormap(index / (n_groups - 1)) for index in range(n_groups)]


def run_simulation(parameters: dict[str, Any]) -> SchellingModel:
    """Run the whole simulation first and return the finished model."""
    model = SchellingModel(parameters)
    model.run(display=False)
    return model


def animate_model(model: SchellingModel, interval: int = 150) -> FuncAnimation:
    """Animate the recorded history of an already finished model."""
    n_groups = model.p.n_groups
    history = model.history
    frame_count = len(history)
    colors = [EMPTY_COLOR, *group_colors(n_groups)]
    labels = ["puste", *(f"grupa {group + 1}" for group in range(n_groups))]
    legend_columns = -(-len(labels) // LEGEND_ROWS)

    # Widen the figure for every extra legend column; the constrained layout
    # keeps room for the title and the legend.
    figure, axis = plt.subplots(
        figsize=(8 + 1.5 * (legend_columns - 1), 8), layout="constrained"
    )
    # Transpose, so the first grid index is drawn on the x axis.
    image = axis.imshow(
        history[0].T,
        cmap=ListedColormap(colors),
        vmin=EMPTY,
        vmax=n_groups - 1,
        origin="lower",
        interpolation="nearest",
    )
    axis.set_xlabel("x")
    axis.set_ylabel("y")
    figure.legend(
        handles=[
            Patch(facecolor=color, edgecolor="gray", label=label)
            for color, label in zip(colors, labels)
        ],
        loc="outside right upper",
        ncol=legend_columns,
        fontsize="small" if len(labels) > LEGEND_ROWS else None,
    )
    title = axis.set_title("")

    def update(frame: int):
        image.set_data(history[frame].T)
        title.set_text(
            f"Schelling - AgentPy - krok {frame} / {frame_count - 1}\n"
            f"zadowoleni: {model.happy_history[frame]:.0%}"
            f" - podobni sąsiedzi: {model.similar_history[frame]:.0%}"
        )
        return image, title

    update(0)
    return FuncAnimation(
        figure,
        update,
        frames=frame_count,
        interval=interval,
        blit=False,
        repeat=True,
    )
