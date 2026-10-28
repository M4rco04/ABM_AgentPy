"""AgentPy model for a two-dimensional boids simulation."""

from __future__ import annotations

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
        self.history: list[np.ndarray] = [self.positions()]

    def positions(self) -> np.ndarray:
        """Return a copy of all boid positions in a stable array shape."""
        return np.asarray(list(self.space.positions.values()), dtype=float).copy()

    def step(self) -> None:
        self.agents.update_velocity()
        self.agents.update_position()
        self.history.append(self.positions())

    def end(self) -> None:
        self.final_positions = self.positions()


def default_parameters() -> dict[str, Any]:
    """Load the default simulation parameters from the JSON configuration."""
    parameters_path = Path(__file__).with_name("parameters.json")
    with parameters_path.open(encoding="utf-8") as parameters_file:
        parameters = json.load(parameters_file)

    return parameters
