"""AgentPy model for a two-dimensional boids simulation."""

import json
from pathlib import Path
from typing import Any

import agentpy as ap
import numpy as np

from .agent import Boid
from .environment import create_environment


class BoidsModel(ap.Model):
    """A flocking model based on local interactions between boids."""

    def setup(self) -> None:
        self.space = create_environment(self)
        self.agents = ap.AgentList(self, self.p.population, Boid)
        self.space.add_agents(self.agents, random=True)
        self.agents.setup_pos(self.space)

        self.history: list[np.ndarray] = []
        self.velocity_history: list[np.ndarray] = []
        self.record_state()

    def positions(self) -> np.ndarray:
        """Return a copy of all boid positions, one row per agent."""
        return np.asarray(list(self.agents.pos), dtype=float).copy()

    def velocities(self) -> np.ndarray:
        """Return a copy of all boid velocities, one row per agent."""
        return np.asarray(list(self.agents.velocity), dtype=float).copy()

    def record_state(self) -> None:
        """Store the current positions and velocities of all boids."""
        self.history.append(self.positions())
        self.velocity_history.append(self.velocities())

    def step(self) -> None:
        self.agents.update_velocity()
        self.agents.update_position()
        self.record_state()

    def end(self) -> None:
        self.final_positions = self.positions()


def default_parameters() -> dict[str, Any]:
    """Load the default simulation parameters from the JSON configuration."""
    parameters_path = Path(__file__).with_name("parameters.json")
    with parameters_path.open(encoding="utf-8") as parameters_file:
        parameters = json.load(parameters_file)

    return parameters
