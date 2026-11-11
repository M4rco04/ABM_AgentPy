"""AgentPy model of diffusion-limited aggregation."""

import json
from pathlib import Path
from typing import Any

import agentpy as ap
import numpy as np

from .agent import Particle
from .environment import create_environment

EMPTY = 0
WALKING = 1
STUCK = 2


class DiffusionLimitedAggregationModel(ap.Model):
    """Random walkers stick to a growing cluster started by a single seed."""

    def setup(self) -> None:
        self.grid = create_environment(self)

        seed = ap.AgentList(self, 1, Particle)
        self.grid.add_agents(seed, positions=[(self.p.h // 2, self.p.w // 2)])
        seed.stuck = True

        walkers = ap.AgentList(self, self.p.n_particles, Particle)
        self.grid.add_agents(walkers, random=True, empty=True)

        self.particles = seed + walkers

        self.history: list[np.ndarray] = []
        self.stuck_history: list[int] = []
        self.record_state()

    def state_grid(self) -> np.ndarray:
        """Return the state of every cell as a 2D array."""
        states = np.full(self.grid.shape, EMPTY, dtype=np.uint8)
        for particle, position in self.grid.positions.items():
            states[position] = STUCK if particle.stuck else WALKING
        return states

    def stuck_count(self) -> int:
        """Return the number of particles that belong to the cluster."""
        return sum(self.particles.stuck)

    def record_state(self) -> None:
        """Store the grid and the cluster size of the current step."""
        self.history.append(self.state_grid())
        self.stuck_history.append(self.stuck_count())

    def step(self) -> None:
        self.particles.shuffle().step()
        self.record_state()

        if all(self.particles.stuck):
            self.stop()


def default_parameters() -> dict[str, Any]:
    """Load the default simulation parameters from the JSON configuration."""
    parameters_path = Path(__file__).with_name("parameters.json")
    with parameters_path.open(encoding="utf-8") as parameters_file:
        parameters = json.load(parameters_file)

    return parameters
