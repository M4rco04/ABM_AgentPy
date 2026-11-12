"""Run a selected simulation and replay it as an animation."""

import argparse

import matplotlib.pyplot as plt


def run_ant() -> None:
    """Compute the Langton's ant simulation, then show the animation."""
    from LangtonAnt.model import default_parameters
    from LangtonAnt.visualization import animate_model, run_simulation

    print("Obliczanie symulacji mrówki Langtona...")
    model = run_simulation(default_parameters())
    print(f"Gotowe: {model.t} kroków. Uruchamiam animację.")

    animation = animate_model(model, interval=30)
    plt.show()
    del animation


def run_boids() -> None:
    """Compute the boids simulation, then show the animation."""
    from Boids.model import default_parameters
    from Boids.visualization import animate_model, run_simulation

    print("Obliczanie symulacji Boids...")
    model = run_simulation(default_parameters())
    print(f"Gotowe: {model.t} kroków. Uruchamiam animację.")

    animation = animate_model(model, interval=35)
    plt.show()
    del animation


def run_brain() -> None:
    """Compute the Brian's Brain simulation, then show the animation."""
    from BriansBrain.model import default_parameters
    from BriansBrain.visualization import animate_model, run_simulation

    print("Obliczanie symulacji Brian's Brain...")
    model = run_simulation(default_parameters())
    print(f"Gotowe: {model.t} kroków. Uruchamiam animację.")

    animation = animate_model(model, interval=100)
    plt.show()
    del animation


def run_dla() -> None:
    """Compute the diffusion-limited aggregation, then show the animation."""
    from DiffusionLimitedAggregation.model import default_parameters
    from DiffusionLimitedAggregation.visualization import (
        animate_model,
        run_simulation,
    )

    print("Obliczanie symulacji DLA...")
    model = run_simulation(default_parameters())
    print(f"Gotowe: {model.t} kroków. Uruchamiam animację.")

    animation = animate_model(model, interval=30)
    plt.show()
    del animation


def run_epidemic() -> None:
    """Compute the epidemic simulation, then show the animation."""
    from Epidemic.model import default_parameters
    from Epidemic.visualization import animate_model, run_simulation

    print("Obliczanie symulacji epidemii...")
    model = run_simulation(default_parameters())
    print(f"Gotowe: {model.t} kroków. Uruchamiam animację.")

    animation = animate_model(model, interval=80)
    plt.show()
    del animation


def run_sand() -> None:
    """Compute the sandpile simulation, then show the animation."""
    from SandStack.model import default_parameters
    from SandStack.visualization import animate_model, run_simulation

    print("Obliczanie symulacji SandStack...")
    model = run_simulation(default_parameters())
    print(f"Gotowe: {model.t} kroków. Uruchamiam animację.")

    animation = animate_model(model, interval=50)
    plt.show()
    del animation


def run_schelling() -> None:
    """Compute the Schelling segregation simulation, then show the animation."""
    from SchellingModel.model import default_parameters
    from SchellingModel.visualization import animate_model, run_simulation

    print("Obliczanie symulacji Schellinga...")
    model = run_simulation(default_parameters())
    print(f"Gotowe: {model.t} kroków. Uruchamiam animację.")

    animation = animate_model(model, interval=150)
    plt.show()
    del animation


SIMULATIONS = {
    "ant": run_ant,
    "boids": run_boids,
    "brain": run_brain,
    "dla": run_dla,
    "epidemic": run_epidemic,
    "sand": run_sand,
    "schelling": run_schelling,
}


def main() -> None:
    """Parse the selected simulation and run it."""
    parser = argparse.ArgumentParser(description="Uruchom symulację AgentPy.")
    parser.add_argument(
        "simulation",
        nargs="?",
        choices=SIMULATIONS,
        default="boids",
        help="symulacja do uruchomienia (domyślnie: boids)",
    )
    args = parser.parse_args()
    SIMULATIONS[args.simulation]()


if __name__ == "__main__":
    main()
