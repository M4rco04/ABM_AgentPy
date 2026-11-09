"""Environment factory and neighbourhood helper for the sandpile model."""

import agentpy as ap

VON_NEUMANN_OFFSETS = ((1, 0), (-1, 0), (0, 1), (0, -1))


def create_environment(model: ap.Model) -> ap.Grid:
    """Create the bounded (non-wrapping) grid used by the model."""
    return ap.Grid(model, (model.p.W, model.p.H), torus=False)


def von_neumann_neighbors(grid: ap.Grid, agent: ap.Agent) -> list[ap.Agent]:
    """Return the agents directly above, below, left and right of ``agent``.

    Cells on the edge of the grid have fewer neighbours.
    """
    x, y = grid.positions[agent]
    width, height = grid.shape
    neighbors = []
    for dx, dy in VON_NEUMANN_OFFSETS:
        nx, ny = x + dx, y + dy
        if not (0 <= nx < width and 0 <= ny < height):
            continue
        neighbors.extend(grid.grid.agents[nx, ny])
    return neighbors
