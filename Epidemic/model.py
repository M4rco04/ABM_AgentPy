"""AgentPy model of an SIR epidemic among randomly walking people."""

import json
from pathlib import Path
from typing import Any

import agentpy as ap
import numpy as np

from .agent import HealthState, Person
from .environment import create_environment

EMPTY = -1


class EpidemicModel(ap.Model):
    """People walk randomly; the infected ones infect their neighbours."""

    def setup(self) -> None:
        self.grid = create_environment(self)
        self.agents = ap.AgentList(self, self.p.population, Person)
        self.grid.add_agents(self.agents, random=True, empty=True)

        self.agents.random(self.p.initial_infected).infect()

        self.history: list[np.ndarray] = []
        self.susceptible_history: list[int] = []
        self.infected_history: list[int] = []
        self.recovered_history: list[int] = []
        self.record_state()

    def state_grid(self) -> np.ndarray:
        """Return the state of every cell as a 2D array (EMPTY for no person)."""
        states = np.full(self.grid.shape, EMPTY, dtype=int)
        for agent, position in self.grid.positions.items():
            states[position] = agent.state.value
        return states

    def count(self, state: HealthState) -> int:
        """Return the number of people in the given state."""
        return sum(agent.state == state for agent in self.agents)

    def record_state(self) -> None:
        """Store the grid and the number of people in every state."""
        self.history.append(self.state_grid())
        self.susceptible_history.append(self.count(HealthState.SUSCEPTIBLE))
        self.infected_history.append(self.count(HealthState.INFECTED))
        self.recovered_history.append(self.count(HealthState.RECOVERED))

    def step(self) -> None:
        self.agents.shuffle().move()
        self.agents.compute_next_state()
        self.agents.apply_next_state()
        self.record_state()

        if self.infected_history[-1] == 0:
            self.stop()


def default_parameters() -> dict[str, Any]:
    """Load the default simulation parameters from the JSON configuration."""
    parameters_path = Path(__file__).with_name("parameters.json")
    with parameters_path.open(encoding="utf-8") as parameters_file:
        parameters = json.load(parameters_file)

    return parameters
