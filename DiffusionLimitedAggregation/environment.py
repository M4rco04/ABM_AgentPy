import agentpy as ap


def create_environment(model: ap.Model) -> ap.Grid:
    return ap.Grid(model, (model.p.h, model.p.w), torus=False, track_empty=True)
