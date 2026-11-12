"""Replay of a finished Langton's ant simulation."""

from typing import Any

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.colors import ListedColormap
from matplotlib.lines import Line2D
from matplotlib.patches import Patch

from .model import LangtonAntModel

# Colors for a white cell, a black cell and the ant itself.
CELL_COLORS = ("#f4f1de", "#14213d")
CELL_LABELS = ("białe", "czarne")
ANT_COLOR = "#e63946"


def run_simulation(parameters: dict[str, Any]) -> LangtonAntModel:
    """Run the whole simulation first and return the finished model."""
    model = LangtonAntModel(parameters)
    model.run(display=False)
    return model


def animate_model(model: LangtonAntModel, interval: int = 30) -> FuncAnimation:
    """Animate the recorded history of an already finished model."""
    history = model.history
    steps = model.history_steps
    ant_positions = model.ant_history
    frame_count = len(history)

    figure, axis = plt.subplots(figsize=(8, 8))
    # Transpose, so the first grid index is drawn on the x axis.
    image = axis.imshow(
        history[0].T,
        cmap=ListedColormap(CELL_COLORS),
        vmin=0,
        vmax=1,
        origin="lower",
        interpolation="nearest",
    )
    (ant_marker,) = axis.plot(
        [], [], marker="o", markersize=6, color=ANT_COLOR, linestyle="none"
    )
    axis.set_xlabel("x")
    axis.set_ylabel("y")
    axis.legend(
        handles=[
            *(
                Patch(facecolor=color, edgecolor="gray", label=label)
                for color, label in zip(CELL_COLORS, CELL_LABELS)
            ),
            Line2D(
                [], [], marker="o", color=ANT_COLOR, linestyle="none", label="mrówka"
            ),
        ],
        loc="upper left",
        bbox_to_anchor=(1.02, 1),
    )
    figure.tight_layout()
    title = axis.set_title("")

    def update(frame: int):
        image.set_data(history[frame].T)
        x, y = ant_positions[frame]
        ant_marker.set_data([x], [y])
        title.set_text(
            f"Mrówka Langtona - AgentPy - krok {steps[frame]} / {steps[-1]}"
            f" - czarne pola: {history[frame].sum()}"
        )
        return image, ant_marker, title

    update(0)
    return FuncAnimation(
        figure,
        update,
        frames=frame_count,
        interval=interval,
        blit=False,
        repeat=True,
    )
