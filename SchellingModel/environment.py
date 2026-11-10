"""Environment factory for the Schelling segregation model."""

import agentpy as ap


def create_environment(model: ap.Model) -> ap.Grid:
    """Create the toroidal grid that keeps track of its empty cells."""
    return ap.Grid(model, (model.p.size, model.p.size), torus=True, track_empty=True)
