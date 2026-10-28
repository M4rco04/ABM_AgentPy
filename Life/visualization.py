"""Visualization helpers for Conway's Game of Life."""

import numpy as np

from Life.model import GameOfLife


def plot_model(model: GameOfLife, axis) -> None:
    """Draw the current Life grid for one animation frame."""
    size = model.p.size
    states = np.zeros((size, size), dtype=int)
    for cell in model.cells:
        x, y = model.grid.positions[cell]
        states[int(y), int(x)] = cell.state

    axis.clear()
    axis.imshow(
        states,
        cmap="binary",
        interpolation="nearest",
        origin="lower",
        vmin=0,
        vmax=1,
    )
    axis.set_title(f"Game of Life - AgentPy - krok {model.t}")
    axis.set_xlabel("x")
    axis.set_ylabel("y")
    axis.set_xticks([])
    axis.set_yticks([])
