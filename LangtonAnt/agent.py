"""Ant agent of Langton's ant and its turning rule."""

import agentpy as ap

# Up, right, down, left - clockwise, so adding 1 to the index turns right.
DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0)]


class Ant(ap.Agent):
    """An ant that turns depending on the cell colour and flips that colour."""

    direction: int

    def setup(self) -> None:
        """Start facing up."""
        self.direction = 0

    def step(self) -> None:
        """Turn, flip the colour of the current cell and move one cell forward.

        The ant turns right on a white cell and left on a black one.
        """
        position = self.model.grid.positions[self]
        is_black = self.model.cells[position]

        if is_black:
            self.direction = (self.direction - 1) % len(DIRECTIONS)
        else:
            self.direction = (self.direction + 1) % len(DIRECTIONS)

        self.model.cells[position] = not is_black
        self.model.grid.move_by(self, DIRECTIONS[self.direction])
