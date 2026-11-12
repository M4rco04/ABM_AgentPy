"""AgentPy model of Langton's ant."""

import json
from pathlib import Path
from typing import Any

import agentpy as ap
import numpy as np

from .agent import Ant
from .environment import create_environment


class LangtonAntModel(ap.Model):
    """A single ant repaints the cells it walks over."""

    def setup(self) -> None:
        self.grid = create_environment(self)
        # Cell colours: False is white, True is black.
        self.cells = np.zeros(self.grid.shape, dtype=bool)

        self.ants = ap.AgentList(self, 1, Ant)
        center = (self.p.size // 2, self.p.size // 2)
        self.grid.add_agents(self.ants, positions=[center])
        self.ant: Ant = self.ants[0]

        self.history: list[np.ndarray] = []
        self.history_steps: list[int] = []
        self.ant_history: list[tuple[int, int]] = []
        self.record_state()

    def record_state(self) -> None:
        """Store the cell colours, the ant position and the step number."""
        self.history.append(self.cells.copy())
        self.history_steps.append(self.t)
        self.ant_history.append(self.grid.positions[self.ant])

    def step(self) -> None:
        self.ants.step()

        if self.t % self.p.record_every == 0 or self.t == self.p.steps:
            self.record_state()


def default_parameters() -> dict[str, Any]:
    """Load the default simulation parameters from the JSON configuration."""
    parameters_path = Path(__file__).with_name("parameters.json")
    with parameters_path.open(encoding="utf-8") as parameters_file:
        parameters = json.load(parameters_file)

    return parameters
