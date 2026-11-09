"""AgentPy model of a sandpile (Bak-Tang-Wiesenfeld)."""

import json
from pathlib import Path
from typing import Any

import agentpy as ap
import numpy as np

from .agent import SandCell
from .environment import create_environment


class SandStack(ap.Model):
    """Grains fall one by one; overloaded cells topple onto neighbours."""

    def setup(self) -> None:
        self.grid = create_environment(self)
        self.agents = ap.AgentList(self, self.p.W * self.p.H, SandCell)
        self.grid.add_agents(self.agents)

        center_field = self.grid.grid.agents[self.p.W // 2, self.p.H // 2]
        self.center_cell: SandCell = next(iter(center_field))

        self.avalanche_sizes: list[int] = []

        self.history: list[np.ndarray] = []
        self.history_steps: list[int] = []
        self.record_state()

    def height_grid(self) -> np.ndarray:
        """Return the number of grains in every cell as a 2D array."""
        heights = np.zeros(self.grid.shape, dtype=int)
        for agent, position in self.grid.positions.items():
            heights[position] = agent.h
        return heights

    def record_state(self) -> None:
        """Store the current heights together with the step number."""
        self.history.append(self.height_grid())
        self.history_steps.append(self.t)

    def drop_target(self) -> SandCell:
        """Choose the cell that receives the next grain."""
        if self.p.drop == "random":
            return self.random.choice(self.agents)
        return self.center_cell

    def relax(self, cell: SandCell) -> int:
        """Topple cells until the pile is stable; return the avalanche size."""
        unstable = [cell]
        topplings = 0
        while unstable:
            current = unstable.pop()
            if not current.is_unstable():
                continue
            for neighbor in current.topple():
                if neighbor.is_unstable():
                    unstable.append(neighbor)
            if current.is_unstable():
                unstable.append(current)
            topplings += 1
        return topplings

    def step(self) -> None:
        cell = self.drop_target()
        cell.h += 1
        self.avalanche_sizes.append(self.relax(cell))

        if self.t % self.p.record_every == 0 or self.t == self.p.steps:
            self.record_state()


def default_parameters() -> dict[str, Any]:
    """Load the default simulation parameters from the JSON configuration."""
    parameters_path = Path(__file__).with_name("parameters.json")
    with parameters_path.open(encoding="utf-8") as parameters_file:
        parameters = json.load(parameters_file)

    return parameters
