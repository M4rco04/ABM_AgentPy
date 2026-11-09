"""Run a selected simulation and replay it as an animation."""

import argparse

import matplotlib.pyplot as plt


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


SIMULATIONS = {
    "boids": run_boids,
    "brain": run_brain,
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
