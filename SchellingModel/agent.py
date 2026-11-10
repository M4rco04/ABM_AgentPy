"""Household agent of the Schelling model and its relocation rule."""

import agentpy as ap


class SchellingAgent(ap.Agent):
    """A household that moves away when too few neighbours share its group."""

    group: int
    share_similar: float
    happy: bool

    def setup(self) -> None:
        """Assign a random group and start as unhappy."""
        self.group = self.model.random.randrange(self.p.n_groups)
        self.share_similar = 0.0
        self.happy = False

    def update_happiness(self) -> None:
        """Compute the share of similar neighbours and decide if happy.

        An agent without neighbours counts as unhappy.
        """
        neighbors = self.model.grid.neighbors(
            self, distance=self.p.neighbor_distance
        ).to_list()
        if neighbors:
            same_group = sum(neighbor.group == self.group for neighbor in neighbors)
            self.share_similar = same_group / len(neighbors)
        else:
            self.share_similar = 0.0
        self.happy = self.share_similar >= self.p.want_similar

    def relocate(self) -> None:
        """Move an unhappy agent to a random empty cell."""
        if self.happy:
            return
        empty_cells = list(self.model.grid.empty)
        if empty_cells:
            self.model.grid.move_to(self, self.model.random.choice(empty_cells))
