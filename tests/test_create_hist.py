from controller.plotting import create_hist

from pathlib import Path

import numpy as np


def test_create_hist() -> None:
    x = np.linspace(-1, 1, 100)
    y = x**2
    data = np.random.randn(100)
    file_path = Path.cwd() / "img/test_hist.png"

    if file_path.exists():
        file_path.unlink()

    create_hist((x, y), data, 7, file_path)

    assert file_path.exists() == True
