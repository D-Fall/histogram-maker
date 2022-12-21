from controller.plotting import create_histogram, save_histogram

from pathlib import Path

import pytest
import numpy as np
from matplotlib.figure import Figure


@pytest.fixture
def fig() -> Figure:
    x = np.linspace(-1, 1, 100)
    y = x**2
    data = np.random.randn(100)

    return create_histogram((x, y), data, 7)


def test_create_histogram(fig: Figure):
    assert isinstance(fig, Figure)


def test_save_histogram(fig: Figure):
    filepath = Path.cwd() / "tests/mock/test_hist.png"

    if filepath.exists():
        filepath.unlink()

    save_histogram(fig, filepath)

    assert filepath.exists()
