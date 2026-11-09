"""Run the boids simulation and replay it as an animation."""

import matplotlib.pyplot as plt

from Boids.model import default_parameters
from Boids.visualization import animate_model, run_simulation


def main() -> None:
    """Compute the whole simulation first, then show the animation."""
    print("Obliczanie symulacji Boids...")
    model = run_simulation(default_parameters())
    print(f"Gotowe: {model.t} kroków. Uruchamiam animację.")

    animation = animate_model(model, interval=35)
    plt.show()
    del animation


if __name__ == "__main__":
    main()
