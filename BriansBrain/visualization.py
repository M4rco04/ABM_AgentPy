"""Replay of a finished Brian's Brain simulation."""

from typing import Any

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.colors import ListedColormap
from matplotlib.patches import Patch

from .agent import CellState
from .model import BriansBrain

# Colors for OFF, ON and DYING, in the order of their values (0, 1, 2).
STATE_COLORS = ("#111111", "#f5f5f5", "#3b82f6")


def run_simulation(parameters: dict[str, Any]) -> BriansBrain:
    """Run the whole simulation first and return the finished model."""
    model = BriansBrain(parameters)
    model.run(display=False)
    return model


def animate_model(model: BriansBrain, interval: int = 100) -> FuncAnimation:
    """Animate the recorded history of an already finished model."""
    history = model.history
    frame_count = len(history)

    figure, axis = plt.subplots(figsize=(8, 8))
    # Transpose, so the first grid index is drawn on the x axis.
    image = axis.imshow(
        history[0].T,
        cmap=ListedColormap(STATE_COLORS),
        vmin=0,
        vmax=len(STATE_COLORS) - 1,
        origin="lower",
        interpolation="nearest",
    )
    axis.set_xlabel("x")
    axis.set_ylabel("y")
    axis.legend(
        handles=[
            Patch(facecolor=STATE_COLORS[state.value], edgecolor="gray",
                  label=state.name)
            for state in CellState
        ],
        loc="upper left",
        bbox_to_anchor=(1.02, 1),
    )
    figure.tight_layout()
    title = axis.set_title("")

    def update(frame: int):
        image.set_data(history[frame].T)
        title.set_text(
            f"Brian's Brain - AgentPy - krok {frame} / {frame_count - 1}"
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
