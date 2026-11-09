"""AgentPy model for the Brian's Brain cellular automaton."""

import json
from pathlib import Path
from typing import Any

import agentpy as ap
import numpy as np

from .agent import BrianCell
from .environment import create_environment


class BriansBrain(ap.Model):
    """A three-state cellular automaton on a wrapping grid."""

    def setup(self) -> None:
        self.grid = create_environment(self)
        self.agents = ap.AgentList(
            self, self.p.size * self.p.size, BrianCell
        )
        self.grid.add_agents(self.agents)
        self.history: list[np.ndarray] = []
        self.record_state()

    def state_grid(self) -> np.ndarray:
        """Return the cell states as a 2D array of numbers (0, 1, 2)."""
        states = np.zeros(self.grid.shape, dtype=int)
        for agent, position in self.grid.positions.items():
            states[position] = agent.state.value
        return states

    def record_state(self) -> None:
        """Store the current state of the whole grid."""
        self.history.append(self.state_grid())

    def step(self) -> None:
        self.agents.compute_next_state()
        self.agents.apply_next_state()
        self.record_state()


def default_parameters() -> dict[str, Any]:
    """Load the default simulation parameters from the JSON configuration."""
    parameters_path = Path(__file__).with_name("parameters.json")
    with parameters_path.open(encoding="utf-8") as parameters_file:
        parameters = json.load(parameters_file)

    return parameters
