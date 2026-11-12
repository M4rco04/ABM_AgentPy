"""Environment factory for the epidemic model."""

import agentpy as ap


def create_environment(model: ap.Model) -> ap.Grid:
    """Create the bounded grid that keeps track of its empty cells."""
    return ap.Grid(model, (model.p.size, model.p.size), torus=False, track_empty=True)
