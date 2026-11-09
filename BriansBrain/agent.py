"""Brian's Brain cell agent and its state rules."""

from enum import Enum

import agentpy as ap


class CellState(Enum):
    """Possible states of a Brian's Brain cell."""

    OFF = 0
    ON = 1
    DYING = 2


class BrianCell(ap.Agent):
    """A single cell that cycles through OFF -> ON -> DYING -> OFF."""

    state: CellState
    next_state: CellState

    def setup(self) -> None:
        """Pick a random initial state."""
        if self.model.random.random() < self.p.initial_off_probability:
            self.state = CellState.OFF
        else:
            self.state = CellState.ON
        self.next_state = self.state

    def compute_next_state(self) -> None:
        """Choose the next state from the current states of the neighbours.

        The new state is only stored in ``next_state``, so every cell sees
        the same, unchanged grid while the whole step is being computed.
        """
        if self.state == CellState.ON:
            self.next_state = CellState.DYING
        elif self.state == CellState.DYING:
            self.next_state = CellState.OFF
        else:
            neighbors = self.model.grid.neighbors(
                self, distance=self.p.neighbor_distance
            )
            neighbors_on = sum(
                neighbor.state == CellState.ON for neighbor in neighbors
            )
            if neighbors_on == 2:
                self.next_state = CellState.ON
            else:
                self.next_state = CellState.OFF

    def apply_next_state(self) -> None:
        """Switch to the state chosen in ``compute_next_state``."""
        self.state = self.next_state
