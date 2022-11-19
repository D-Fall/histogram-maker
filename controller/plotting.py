from pathlib import Path

import matplotlib.pyplot as plt
from numpy import array


def create_hist(
    func_axes: tuple[array, array],
    data: list[float],
    bins: int,
    filename: str,
) -> None:
    if not filename.endswith(".png"):
        filename += ".png"

    path: Path = Path.cwd() / f"img/{filename}"

    plt.style.use(["science", "notebook", "grid"])

    plt.hist(data, bins=bins, density=True)
    plt.plot(*func_axes, "r", label="Normal distribution")
    plt.xlabel("$x$")
    plt.ylabel("Density")
    plt.legend()
    plt.savefig(path, dpi=200)
