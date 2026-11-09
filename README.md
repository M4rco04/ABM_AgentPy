# ABM AgentPy — Boids simulation

A flocking (boids) model built with
[AgentPy](https://agentpy.readthedocs.io/). Each boid only sees its nearest
neighbours and uses them to adjust its direction by applying:

- **separation** — avoid agents that are too close (radius `inner_radius`),
- **alignment** — match the flight direction of neighbours (radius `outer_radius`),
- **cohesion** — move towards the centre of the local group (radius `outer_radius`),
- **border avoidance** — turn away when getting close to the edge of the world.

The world is a two-dimensional toroidal space: a boid leaving one edge
reappears on the opposite side. The number of boids stays constant for the
whole simulation and is set by the `population` parameter.

## Requirements

- Python 3.13 (3.12 also works),
- packages from [`requirements.txt`](requirements.txt): `agentpy`, `numpy`, `matplotlib`.

## Installation

From the repository root:

```powershell
py -3.13 -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

## Running

```powershell
python .\main.py
```

The program first computes the whole simulation (the number of steps comes
from the `steps` parameter) and only then opens a window with the animation.
The animation is replayed from the recorded history, so it runs smoothly no
matter how long the computation took, and it loops after the last step. Each
boid is drawn as an arrow pointing in its direction of flight.

## Parameters

Parameters are stored in [`Boids/parameters.json`](Boids/parameters.json).
The `default_parameters()` function in [`Boids/model.py`](Boids/model.py)
loads this file regardless of the directory the program is run from.

| Parameter             | Meaning                                                  |
| --------------------- | -------------------------------------------------------- |
| `size`                | side length of the world                                 |
| `ndim`                | number of dimensions (the visualization supports 2)      |
| `population`          | number of boids                                          |
| `steps`               | number of simulation steps                               |
| `inner_radius`        | separation range                                         |
| `outer_radius`        | alignment and cohesion range                             |
| `border_distance`     | distance from the edge at which border avoidance starts  |
| `border_strength`     | strength of border avoidance                             |
| `cohesion_strength`   | strength of cohesion                                     |
| `separation_strength` | strength of separation                                   |
| `alignment_strength`  | strength of alignment                                    |
| `seed`                | random seed — the same seed gives the same run           |

## Project structure

| File | Contents |
| --- | --- |
| [`main.py`](main.py) | entry point: computes the simulation and shows the animation |
| [`Boids/agent.py`](Boids/agent.py) | the `Boid` class (flocking rules: `update_velocity`, `update_position`) and the `normalize` function |
| [`Boids/environment.py`](Boids/environment.py) | creates the toroidal `ap.Space` |
| [`Boids/model.py`](Boids/model.py) | `BoidsModel` — runs the steps and records position (`history`) and velocity (`velocity_history`) history |
| [`Boids/visualization.py`](Boids/visualization.py) | `run_simulation()` computes the whole model, `animate_model()` replays the recorded history |
| [`Boids/parameters.json`](Boids/parameters.json) | default parameters |

## Using it from your own code

```python
import matplotlib.pyplot as plt

from Boids.model import default_parameters
from Boids.visualization import animate_model, run_simulation

parameters = default_parameters()
parameters["population"] = 200

model = run_simulation(parameters)   # computation
animation = animate_model(model)     # animation from the recorded history
plt.show()
```
