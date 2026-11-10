# ABM AgentPy

Agent-based simulations built with [AgentPy](https://agentpy.readthedocs.io/):

- **Boids** — flocking behaviour of birds,
- **Brian's Brain** — a three-state cellular automaton,
- **SandStack** — a sandpile model (Bak–Tang–Wiesenfeld),
- **Schelling** — Schelling's segregation model.

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
python .\main.py sand    # SandStack
python .\main.py schelling  # Schelling segregation
python .\main.py         # same as "boids"
python .\main.py --help  # list available simulations
```

| Argument | Simulation    | Package                        |
| -------- | ------------- | ------------------------------ |
| `boids`  | Boids         | [`Boids/`](Boids/)             |
| `brain`  | Brian's Brain | [`BriansBrain/`](BriansBrain/) |
| `sand`   | SandStack     | [`SandStack/`](SandStack/)     |
| `schelling` | Schelling  | [`SchellingModel/`](SchellingModel/) |

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

## SandStack

A sandpile on a bounded square grid. Each cell is an agent holding `h` grains
of sand. In every step:

1. One grain falls on the grid — on the centre cell or on a random cell.
2. Every cell with 4 or more grains **topples**: it loses 4 grains and gives
   one to each of its 4 von Neumann neighbours (up, down, left, right).
3. Toppling repeats until no cell has 4 or more grains. One dropped grain can
   start a chain reaction (an **avalanche**) that spreads far across the grid.

The grid does not wrap: grains toppled over the edge fall off and are lost.
After an avalanche every cell holds 0–3 grains, shown in four colours.

- With `drop: "center"` the pile grows from the middle into a symmetric
  fractal pattern.
- With `drop: "random"` the grid fills up evenly until it reaches a critical
  state, where avalanches of all sizes occur (self-organised criticality).

The number of topplings caused by each grain is stored in
`model.avalanche_sizes`.

### SandStack parameters

Stored in [`SandStack/parameters.json`](SandStack/parameters.json).

| Parameter | Meaning |
| --- | --- |
| `W` | grid width |
| `H` | grid height |
| `steps` | number of simulation steps = number of dropped grains |
| `drop` | where grains fall: `"center"` or `"random"` |
| `record_every` | save a frame every N steps (the last step is always saved) |
| `seed` | random seed — the same seed gives the same run |

With the default settings (61×61, 5000 grains, `"center"`) the computation
takes several seconds. In `"center"` mode the time grows quickly with the
number of grains, because avalanches get larger as the pile grows.

## Schelling

Schelling's segregation model on a wrapping (toroidal) square grid. Each agent
belongs to one of `n_groups` groups and lives in one cell; some cells stay
empty. In every step:

1. Every **unhappy** agent moves to a random empty cell.
2. Every agent counts its neighbours and computes the share that belong to its
   own group. It is **happy** when this share is at least `want_similar`.
   An agent with no neighbours counts as unhappy.

The simulation stops early once every agent is happy. Even a mild preference
(for example 50% similar neighbours) leads to strongly separated clusters —
the average share of similar neighbours ends up much higher than required.
The animation title shows the share of happy agents and this average share.

### Schelling parameters

Stored in [`SchellingModel/parameters.json`](SchellingModel/parameters.json).

| Parameter | Meaning |
| --- | --- |
| `size` | side length of the grid (`size * size` cells) |
| `agents_count` | number of agents; must be lower than `size * size`, so some cells stay empty |
| `n_groups` | number of groups (any number; colors are generated automatically above 5) |
| `neighbor_distance` | neighbourhood radius (1 = the 8 surrounding cells) |
| `want_similar` | minimal share of same-group neighbours an agent needs to be happy (0–1) |
| `steps` | maximal number of simulation steps |
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
| [`SandStack/agent.py`](SandStack/agent.py) | the `SandCell` class with the toppling rule (`is_unstable`, `topple`) |
| [`SandStack/environment.py`](SandStack/environment.py) | creates the bounded `ap.Grid` and finds von Neumann neighbours (`von_neumann_neighbors`) |
| [`SandStack/model.py`](SandStack/model.py) | `SandStack` — drops grains, runs avalanches and records the heights (`history`, `history_steps`) |
| [`SandStack/visualization.py`](SandStack/visualization.py) | `run_simulation()` computes the whole model, `animate_model()` replays the recorded history |
| [`SchellingModel/agent.py`](SchellingModel/agent.py) | the `SchellingAgent` class (`update_happiness`, `relocate`) |
| [`SchellingModel/environment.py`](SchellingModel/environment.py) | creates the toroidal `ap.Grid` that tracks empty cells |
| [`SchellingModel/model.py`](SchellingModel/model.py) | `SchellingModel` — moves unhappy agents and records the grid of groups (`history`) and statistics (`happy_history`, `similar_history`) |
| [`SchellingModel/visualization.py`](SchellingModel/visualization.py) | `run_simulation()` computes the whole model, `animate_model()` replays the recorded history |

## Using it from your own code

All packages expose the same functions:

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

For the other simulations, import from `BriansBrain.*`, `SandStack.*` or `SchellingModel.*`
instead.
