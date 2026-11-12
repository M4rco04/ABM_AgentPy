"""Environment factory for Langton's ant."""

import agentpy as ap


def create_environment(model: ap.Model) -> ap.Grid:
    """Create the toroidal grid the ant walks on."""
    return ap.Grid(model, (model.p.size, model.p.size), torus=True)
