# ABM AgentPy

Agent-based simulations built with [AgentPy](https://agentpy.readthedocs.io/):

- **Boids** — flocking behaviour of birds,
- **Brian's Brain** — a three-state cellular automaton.

Every simulation is computed in full first, and only then replayed as an
animation from the recorded history. This keeps the animation smooth no matter
how long the computation took. The animation loops after the last step.

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

Choose the simulation with a command-line argument:

```powershell
python .\main.py boids   # Boids (default)
python .\main.py brain   # Brian's Brain
python .\main.py         # same as "boids"
python .\main.py --help  # list available simulations
```

| Argument | Simulation    | Package                        |
| -------- | ------------- | ------------------------------ |
| `boids`  | Boids         | [`Boids/`](Boids/)             |
| `brain`  | Brian's Brain | [`BriansBrain/`](BriansBrain/) |

Each package loads its parameters from its own `parameters.json` through
`default_parameters()`, regardless of the directory the program is run from.

## Boids

Each boid only sees its nearest neighbours and uses them to adjust its
direction by applying:

- **separation** — avoid agents that are too close (radius `inner_radius`),
- **alignment** — match the flight direction of neighbours (radius `outer_radius`),
- **cohesion** — move towards the centre of the local group (radius `outer_radius`),
- **border avoidance** — turn away when getting close to the edge of the world.

The world is a two-dimensional toroidal space: a boid leaving one edge
reappears on the opposite side. The number of boids stays constant for the
whole simulation. Each boid is drawn as an arrow pointing in its direction of
flight.

### Boids parameters

Stored in [`Boids/parameters.json`](Boids/parameters.json).

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

## Brian's Brain

A cellular automaton on a wrapping (toroidal) square grid. Each cell is an
agent in one of three states:

| State   | Colour | Next state                                              |
| ------- | ------ | ------------------------------------------------------- |
| `OFF`   | black  | `ON` if exactly 2 neighbours are `ON`, otherwise `OFF`  |
| `ON`    | white  | always `DYING`                                          |
| `DYING` | blue   | always `OFF`                                            |

Because `ON` cells always become `DYING` and cannot stay on, the automaton
produces moving patterns ("gliders") instead of settling into still shapes.

### Brian's Brain parameters

Stored in [`BriansBrain/parameters.json`](BriansBrain/parameters.json).

| Parameter | Meaning |
| --- | --- |
| `size` | side length of the grid; the model creates `size * size` cells, one per field |
| `steps` | number of simulation steps |
| `initial_off_probability` | probability that a cell starts as `OFF` (otherwise `ON`) |
| `neighbor_distance` | neighbourhood radius (1 = the 8 surrounding cells) |
| `seed` | random seed — the same seed gives the same run |

## Project structure

| File | Contents |
| --- | --- |
| [`main.py`](main.py) | entry point: parses the chosen simulation, computes it and shows the animation |
| [`Boids/agent.py`](Boids/agent.py) | the `Boid` class (flocking rules: `update_velocity`, `update_position`) and the `normalize` function |
| [`Boids/environment.py`](Boids/environment.py) | creates the toroidal `ap.Space` |
| [`Boids/model.py`](Boids/model.py) | `BoidsModel` — runs the steps and records position (`history`) and velocity (`velocity_history`) history |
| [`Boids/visualization.py`](Boids/visualization.py) | `run_simulation()` computes the whole model, `animate_model()` replays the recorded history |
| [`BriansBrain/agent.py`](BriansBrain/agent.py) | `CellState` and the `BrianCell` class with the state rules |
| [`BriansBrain/environment.py`](BriansBrain/environment.py) | creates the toroidal `ap.Grid` |
| [`BriansBrain/model.py`](BriansBrain/model.py) | `BriansBrain` — runs the steps and records the grid of states (`history`) |
| [`BriansBrain/visualization.py`](BriansBrain/visualization.py) | `run_simulation()` computes the whole model, `animate_model()` replays the recorded history |

## Using it from your own code

Both packages expose the same functions:

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

For Brian's Brain, import from `BriansBrain.model` and
`BriansBrain.visualization` instead.
