"""Replay of a finished epidemic simulation."""

from typing import Any

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.colors import ListedColormap
from matplotlib.patches import Patch

from .agent import HealthState
from .model import EMPTY, EpidemicModel

# Colors for an empty cell and for a susceptible, infected and recovered person.
EMPTY_COLOR = "#f5f5f5"
STATE_COLORS = ("#3a7ca5", "#e63946", "#8d99ae")
STATE_LABELS = ("podatni", "zakażeni", "ozdrowiali")


def run_simulation(parameters: dict[str, Any]) -> EpidemicModel:
    """Run the whole simulation first and return the finished model."""
    model = EpidemicModel(parameters)
    model.run(display=False)
    return model


def animate_model(model: EpidemicModel, interval: int = 80) -> FuncAnimation:
    """Animate the recorded history of an already finished model.

    The left panel shows the grid, the right one the number of people in
    every state, with a vertical line marking the current step.
    """
    history = model.history
    frame_count = len(history)
    counts = (
        model.susceptible_history,
        model.infected_history,
        model.recovered_history,
    )

    figure, (grid_axis, curve_axis) = plt.subplots(
        1, 2, figsize=(14, 7), layout="constrained"
    )

    # Transpose, so the first grid index is drawn on the x axis.
    image = grid_axis.imshow(
        history[0].T,
        cmap=ListedColormap([EMPTY_COLOR, *STATE_COLORS]),
        vmin=EMPTY,
        vmax=HealthState.RECOVERED.value,
        origin="lower",
        interpolation="nearest",
    )
    grid_axis.set_xlabel("x")
    grid_axis.set_ylabel("y")
    title = grid_axis.set_title("")

    # The curves never change, so they are drawn once; only the marker moves.
    for count, color in zip(counts, STATE_COLORS):
        curve_axis.plot(count, color=color, linewidth=2)
    marker = curve_axis.axvline(0, color="black", linewidth=1, linestyle="--")
    curve_axis.set_xlim(0, max(frame_count - 1, 1))
    curve_axis.set_ylim(0, model.p.population)
    curve_axis.set_xlabel("krok")
    curve_axis.set_ylabel("liczba osób")
    curve_axis.set_title("Przebieg epidemii")
    curve_axis.grid(alpha=0.3)

    figure.legend(
        handles=[
            Patch(facecolor=color, edgecolor="gray", label=label)
            for color, label in zip(
                (EMPTY_COLOR, *STATE_COLORS), ("puste", *STATE_LABELS)
            )
        ],
        loc="outside right upper",
    )

    def update(frame: int):
        image.set_data(history[frame].T)
        marker.set_xdata([frame, frame])
        title.set_text(
            f"Epidemia - AgentPy - krok {frame} / {frame_count - 1}\n"
            + " - ".join(
                f"{label}: {count[frame]}"
                for label, count in zip(STATE_LABELS, counts)
            )
        )
        return image, marker, title

    update(0)
    return FuncAnimation(
        figure,
        update,
        frames=frame_count,
        interval=interval,
        blit=False,
        repeat=True,
    )
