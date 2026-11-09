"""Sandpile cell agent and its toppling rule."""

import agentpy as ap

from .environment import von_neumann_neighbors

TOPPLE_THRESHOLD = 4


class SandCell(ap.Agent):
    """A grid cell holding a stack of sand grains."""

    h: int

    def setup(self) -> None:
        """Start with an empty cell."""
        self.h = 0

    def is_unstable(self) -> bool:
        """Return True when the stack is too high and must topple."""
        return self.h >= TOPPLE_THRESHOLD

    def topple(self) -> list["SandCell"]:
        """Give one grain to each neighbour and return those neighbours.

        On the edge of the grid some grains fall off and are lost.
        """
        self.h -= TOPPLE_THRESHOLD
        neighbors = von_neumann_neighbors(self.model.grid, self)
        for neighbor in neighbors:
            neighbor.h += 1
        return neighbors
