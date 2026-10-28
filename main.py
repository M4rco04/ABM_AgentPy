"""Run one of the available AgentPy simulations."""

import argparse

import agentpy as ap
import matplotlib.pyplot as plt

from Boids.model import BoidsModel, default_parameters as boids_parameters
from Boids.visualization import plot_model
from Life.model import GameOfLife, default_parameters as life_parameters
from Life.visualization import plot_model as plot_life_model


def main() -> None:
    """Parse the selected simulation and display its animation."""
    parser = argparse.ArgumentParser(description="Uruchom symulację AgentPy.")
    parser.add_argument(
        "simulation",
        nargs="?",
        choices=("boids", "life"),
        default="boids",
        help="symulacja do uruchomienia (domyślnie: boids)",
    )
    args = parser.parse_args()

    if args.simulation == "life":
        model = GameOfLife(life_parameters())
        plot_function = plot_life_model
        interval = 150
    else:
        model = BoidsModel(boids_parameters())
        plot_function = plot_model
        interval = 35

    figure, axis = plt.subplots(figsize=(8, 8))
    close_figure = plt.close
    plt.close = lambda *_, **__: None
    try:
        _ = ap.animate(
            model,
            figure,
            axis,
            plot_function,
            blit=False,
            interval=interval,
            repeat=True,
        )
    finally:
        plt.close = close_figure

    plt.show()


if __name__ == "__main__":
    main()
