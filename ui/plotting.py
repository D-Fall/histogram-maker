from pathlib import Path

import matplotlib.pyplot as plt
from numpy import array


def plot_and_save_hist(
    func_axes: tuple[array, array],
    data: list[float],
    bins: int,
    path: Path,
) -> None:
    plt.style.use(["science", "notebook", "grid"])

    plt.hist(data, bins=bins, density=True)
    plt.plot(*func_axes, "r", label="Normal distribution")
    plt.xlabel("$x$")
    plt.ylabel("Density")
    plt.legend()
    plt.savefig(path, dpi=200)
