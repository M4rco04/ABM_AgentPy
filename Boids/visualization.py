import numpy as np
from Boids.model import BoidsModel

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