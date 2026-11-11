"""Replay of a finished diffusion-limited aggregation simulation."""

from typing import Any

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.colors import ListedColormap
from matplotlib.patches import Patch

from .model import EMPTY, STUCK, DiffusionLimitedAggregationModel

# Colors for an empty cell, a walking particle and a stuck particle.
STATE_COLORS = ("#14213d", "#3a7ca5", "#f4f1de")
STATE_LABELS = ("puste", "błądzące", "przyklejone")


def run_simulation(parameters: dict[str, Any]) -> DiffusionLimitedAggregationModel:
    """Run the whole simulation first and return the finished model."""
    model = DiffusionLimitedAggregationModel(parameters)
    model.run(display=False)
    return model


def animate_model(
    model: DiffusionLimitedAggregationModel, interval: int = 30
) -> FuncAnimation:
    """Animate the recorded history of an already finished model."""
    history = model.history
    frame_count = len(history)
    particle_count = len(model.particles)

    figure, axis = plt.subplots(figsize=(8, 8))
    # Transpose, so the first grid index is drawn on the x axis.
    image = axis.imshow(
        history[0].T,
        cmap=ListedColormap(STATE_COLORS),
        vmin=EMPTY,
        vmax=STUCK,
        origin="lower",
        interpolation="nearest",
    )
    axis.set_xlabel("x")
    axis.set_ylabel("y")
    axis.legend(
        handles=[
            Patch(facecolor=color, edgecolor="gray", label=label)
            for color, label in zip(STATE_COLORS, STATE_LABELS)
        ],
        loc="upper left",
        bbox_to_anchor=(1.02, 1),
    )
    figure.tight_layout()
    title = axis.set_title("")

    def update(frame: int):
        image.set_data(history[frame].T)
        title.set_text(
            f"DLA - AgentPy - krok {frame} / {frame_count - 1}"
            f" - przyklejone: {model.stuck_history[frame]} / {particle_count}"
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
