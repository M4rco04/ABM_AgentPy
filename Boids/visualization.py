"""Replay of a finished boids simulation."""

from typing import Any

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation

from .agent import normalize
from .model import BoidsModel


def run_simulation(parameters: dict[str, Any]) -> BoidsModel:
    """Run the whole simulation first and return the finished model."""
    model = BoidsModel(parameters)
    model.run(display=False)
    return model


def directions(velocities: np.ndarray) -> np.ndarray:
    """Turn the stored velocities into unit vectors used for the arrows."""
    return np.asarray([normalize(velocity) for velocity in velocities])


def animate_model(model: BoidsModel, interval: int = 35) -> FuncAnimation:
    """Animate the recorded history of an already finished model."""
    positions = model.history
    velocities = model.velocity_history
    frame_count = len(positions)

    figure, axis = plt.subplots(figsize=(8, 8))
    axis.set_xlim(0, model.p.size)
    axis.set_ylim(0, model.p.size)
    axis.set_aspect("equal")
    axis.set_xlabel("x")
    axis.set_ylabel("y")
    axis.grid(alpha=0.2)

    start_directions = directions(velocities[0])
    arrows = axis.quiver(
        positions[0][:, 0],
        positions[0][:, 1],
        start_directions[:, 0],
        start_directions[:, 1],
        color="tab:blue",
        angles="xy",
        scale_units="xy",
        scale=0.4,
        pivot="middle",
        width=0.006,
    )
    title = axis.set_title("")

    def update(frame: int):
        frame_directions = directions(velocities[frame])
        arrows.set_offsets(positions[frame])
        arrows.set_UVC(frame_directions[:, 0], frame_directions[:, 1])
        title.set_text(f"Boids - AgentPy - krok {frame} / {frame_count - 1}")
        return arrows, title

    update(0)
    return FuncAnimation(
        figure,
        update,
        frames=frame_count,
        interval=interval,
        blit=False,
        repeat=True,
    )
