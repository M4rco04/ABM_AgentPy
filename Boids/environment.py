"""Environment factory for the boids model."""

import agentpy as ap


def create_environment(model: ap.Model) -> ap.Space:
    """Create the continuous, wrapping 2D world used by the model."""
    return ap.Space(model, shape=[model.p.size] * model.p.ndim, torus=True)
