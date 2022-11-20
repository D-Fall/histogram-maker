import pytest

from controller.data_process import get_stats
from numpy.random import randn


def test_get_stats() -> None:
    mean, std = get_stats(randn(100))
    assert mean == pytest.approx(0, abs=0.5)
    assert std == pytest.approx(1, rel=0.5)
