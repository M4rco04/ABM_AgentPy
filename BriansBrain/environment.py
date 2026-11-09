"""Environment factory for the Brian's Brain model."""

import agentpy as ap


def create_environment(model: ap.Model) -> ap.Grid:
    """Create the square, wrapping grid used by the model."""
    return ap.Grid(model, (model.p.size, model.p.size), torus=True)
