"""AgentPy model for Conway's Game of Life."""

import json
from pathlib import Path
from typing import Any

import agentpy as ap

from Life.cell import Cell


class GameOfLife(ap.Model):
    """A two-dimensional cellular automaton with toroidal boundaries."""

    def setup(self) -> None:
        size = self.p.size
        self.grid = ap.Grid(self, (size, size), torus=True)
        self.cells = ap.AgentList(self, size * size, Cell)
        self.grid.add_agents(self.cells, positions=self.grid.positions)

    def step(self) -> None:
        self.cells.calculate_next_state()
        self.cells.apply_next_state()


def default_parameters() -> dict[str, Any]:
    """Load the default simulation parameters from the JSON configuration."""
    parameters_path = Path(__file__).with_name("parameters.json")
    with parameters_path.open(encoding="utf-8") as parameters_file:
        return json.load(parameters_file)