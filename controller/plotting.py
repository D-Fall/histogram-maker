from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from numpy import array


def create_histogram(
    func_axes: tuple[array, array],
    data: list[float],
    bins: int,
) -> Figure:
    """
    Create the histogram png file.
    """
    plt.style.use(["science", "notebook", "grid"])

    fig, ax = plt.subplots()

    ax.hist(data, bins=bins, density=True)
    ax.plot(*func_axes, "r", label="Normal distribution")
    ax.set_xlabel("$x$")
    ax.set_ylabel("Density")
    ax.legend()

    return fig


def save_histogram(fig: Figure, filepath: Path) -> None:
    fig.savefig(filepath, dpi=200)
