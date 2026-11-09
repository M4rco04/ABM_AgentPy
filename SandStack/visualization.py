"""Replay of a finished sandpile simulation."""

from typing import Any

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.colors import ListedColormap
from matplotlib.patches import Patch

from .agent import TOPPLE_THRESHOLD
from .model import SandStack

# Colors for 0, 1, 2 and 3 grains (a stable cell never holds more).
HEIGHT_COLORS = ("#14213d", "#3a7ca5", "#e9c46a", "#f4f1de")
HEIGHT_LABELS = ("0 ziaren", "1 ziarno", "2 ziarna", "3 ziarna")


def run_simulation(parameters: dict[str, Any]) -> SandStack:
    """Run the whole simulation first and return the finished model."""
    model = SandStack(parameters)
    model.run(display=False)
    return model


def animate_model(model: SandStack, interval: int = 50) -> FuncAnimation:
    """Animate the recorded history of an already finished model."""
    history = model.history
    steps = model.history_steps
    frame_count = len(history)

    figure, axis = plt.subplots(figsize=(8, 8))
    # Transpose, so the first grid index is drawn on the x axis.
    image = axis.imshow(
        history[0].T,
        cmap=ListedColormap(HEIGHT_COLORS),
        vmin=0,
        vmax=TOPPLE_THRESHOLD - 1,
        origin="lower",
        interpolation="nearest",
    )
    axis.set_xlabel("x")
    axis.set_ylabel("y")
    axis.legend(
        handles=[
            Patch(facecolor=color, edgecolor="gray", label=label)
            for color, label in zip(HEIGHT_COLORS, HEIGHT_LABELS)
        ],
        loc="upper left",
        bbox_to_anchor=(1.02, 1),
    )
    figure.tight_layout()
    title = axis.set_title("")

    def update(frame: int):
        image.set_data(history[frame].T)
        title.set_text(
            f"SandStack - AgentPy - krok {steps[frame]} / {steps[-1]}"
            f" - ziaren: {history[frame].sum()}"
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
