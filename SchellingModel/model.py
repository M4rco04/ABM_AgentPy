"""AgentPy model of Schelling's segregation."""

import json
from pathlib import Path
from typing import Any

import agentpy as ap
import numpy as np

from .agent import SchellingAgent
from .environment import create_environment

EMPTY = -1


class SchellingModel(ap.Model):
    """Unhappy agents move to random empty cells until everyone is happy."""

    def setup(self) -> None:
        self.grid = create_environment(self)
        self.agents = ap.AgentList(self, self.p.agents_count, SchellingAgent)
        self.grid.add_agents(self.agents, random=True, empty=True)
        self.agents.update_happiness()

        self.history: list[np.ndarray] = []
        self.happy_history: list[float] = []
        self.similar_history: list[float] = []
        self.record_state()

    def group_grid(self) -> np.ndarray:
        """Return the group of every cell as a 2D array (EMPTY for no agent)."""
        groups = np.full(self.grid.shape, EMPTY, dtype=int)
        for agent, position in self.grid.positions.items():
            groups[position] = agent.group
        return groups

    def happy_share(self) -> float:
        """Return the fraction of happy agents."""
        return sum(self.agents.happy) / len(self.agents)

    def mean_similar_share(self) -> float:
        """Return the average share of similar neighbours (segregation level)."""
        return sum(self.agents.share_similar) / len(self.agents)

    def record_state(self) -> None:
        """Store the grid and the summary statistics of the current step."""
        self.history.append(self.group_grid())
        self.happy_history.append(self.happy_share())
        self.similar_history.append(self.mean_similar_share())

    def step(self) -> None:
        self.agents.relocate()
        self.agents.update_happiness()
        self.record_state()

        if all(self.agents.happy):
            self.stop()


def default_parameters() -> dict[str, Any]:
    """Load the default simulation parameters from the JSON configuration."""
    parameters_path = Path(__file__).with_name("parameters.json")
    with parameters_path.open(encoding="utf-8") as parameters_file:
        parameters = json.load(parameters_file)

    return parameters
