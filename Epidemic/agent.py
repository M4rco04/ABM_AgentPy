"""Person agent of the epidemic model and its SIR state rules."""

from enum import Enum

import agentpy as ap

# The 8 surrounding cells a person can walk to.
MOVES = [(0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 1), (-1, 0)]


class HealthState(Enum):
    """Possible health states of a person."""

    SUSCEPTIBLE = 0
    INFECTED = 1
    RECOVERED = 2


class Person(ap.Agent):
    """A person that walks randomly and goes through S -> I -> R."""

    state: HealthState
    next_state: HealthState

    def setup(self) -> None:
        """Start as susceptible."""
        self.state = HealthState.SUSCEPTIBLE
        self.next_state = HealthState.SUSCEPTIBLE

    def infect(self) -> None:
        """Make the person infected right away (used for the first cases)."""
        self.state = HealthState.INFECTED
        self.next_state = HealthState.INFECTED

    def move(self) -> None:
        """Walk to a random surrounding cell.

        The person stays in place if that cell is occupied or outside the grid.
        """
        move = self.model.random.choice(MOVES)
        p0, p1 = self.model.grid.positions[self]
        new_position = (p0 + move[0], p1 + move[1])
        if new_position in self.model.grid.empty:
            self.model.grid.move_to(self, new_position)

    def compute_next_state(self) -> None:
        """Choose the next state from the current states of the neighbours.

        The new state is only stored in ``next_state``, so every person sees
        the same, unchanged states while the whole step is being computed.
        """
        if self.state == HealthState.SUSCEPTIBLE:
            neighbors = self.model.grid.neighbors(
                self, distance=self.p.neighbor_distance
            )
            infected_neighbors = sum(
                neighbor.state == HealthState.INFECTED for neighbor in neighbors
            )
            # Every infected neighbour is a separate chance to get infected.
            for _ in range(infected_neighbors):
                if self.model.random.random() < self.p.infection_probability:
                    self.next_state = HealthState.INFECTED
                    break
        elif self.state == HealthState.INFECTED:
            if self.model.random.random() < self.p.recovery_probability:
                self.next_state = HealthState.RECOVERED

    def apply_next_state(self) -> None:
        """Switch to the state chosen in ``compute_next_state``."""
        self.state = self.next_state
