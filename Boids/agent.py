"""Boid agent and flocking rules."""

import agentpy as ap
import numpy as np


def normalize(vector: np.ndarray) -> np.ndarray:
    """Return a unit vector, or the original vector when it has no length."""
    length = np.linalg.norm(vector)
    if length == 0:
        return vector
    return vector / length


class Boid(ap.Agent):
    """An agent that follows the three classic boids rules."""

    velocity: np.ndarray

    def setup(self) -> None:
        self.velocity = normalize(self.model.nprandom.random(self.p.ndim) - 0.5)

    def setup_pos(self, space: ap.Space) -> None:
        self.space = space
        self.neighbors = space.neighbors
        self.pos = space.positions[self]

    def update_velocity(self) -> None:
        """Calculate the next direction from the current world state."""
        position = self.pos
        neighbors = self.neighbors(self, distance=self.p.outer_radius)
        neighbor_count = len(neighbors)

        if neighbor_count:
            neighbor_positions = np.asarray(list(neighbors.pos))
            neighbor_velocities = np.asarray(list(neighbors.velocity))

            center = neighbor_positions.mean(axis=0)
            cohesion = (center - position) * self.p.cohesion_strength

            average_velocity = neighbor_velocities.mean(axis=0)
            alignment = (
                average_velocity - self.velocity
            ) * self.p.alignment_strength
        else:
            cohesion = np.zeros(self.p.ndim)
            alignment = np.zeros(self.p.ndim)

        separation = np.zeros(self.p.ndim)
        for neighbor in self.neighbors(self, distance=self.p.inner_radius):
            offset = neighbor.pos - position
            distance = np.linalg.norm(offset)
            if distance > 0:
                separation -= offset / distance
        separation *= self.p.separation_strength

        border = np.zeros(self.p.ndim)
        for dimension in range(self.p.ndim):
            if position[dimension] < self.p.border_distance:
                border[dimension] += self.p.border_strength
            elif position[dimension] > self.space.shape[dimension] - self.p.border_distance:
                border[dimension] -= self.p.border_strength

        self.velocity = normalize(self.velocity + cohesion + alignment + separation + border)

    def update_position(self) -> None:
        """Move the agent after all agents have chosen their new direction."""
        self.space.move_by(self, self.velocity)
