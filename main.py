"""Run and animate the boids simulation."""

from __future__ import annotations

import agentpy as ap
import matplotlib.pyplot as plt
import numpy as np

from Boids.model import BoidsModel, default_parameters


def plot_model(model: BoidsModel, axis) -> None:
    """Draw the current AgentPy model state for one animation frame."""
    positions = np.asarray(list(model.space.positions.values()))
    axis.scatter(
        positions[:, 0],
        positions[:, 1],
        s=22,
        color="tab:blue",
    )
    axis.set_xlim(0, model.p.size)
    axis.set_ylim(0, model.p.size)
    axis.set_aspect("equal")
    axis.set_title(f"Boids - AgentPy - krok {model.t}")
    axis.set_xlabel("x")
    axis.set_ylabel("y")
    axis.grid(alpha=0.2)


def main() -> None:
    model = BoidsModel(default_parameters())
    figure, axis = plt.subplots(figsize=(8, 8))
    close_figure = plt.close
    plt.close = lambda *args, **kwargs: None
    try:
        animation = ap.animate(
            model,
            figure,
            axis,
            plot_model,
            blit=False,
            interval=35,
            repeat=True,
        )
    finally:
        plt.close = close_figure

    plt.show()


if __name__ == "__main__":
    main()
