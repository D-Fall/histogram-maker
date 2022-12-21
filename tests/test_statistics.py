import pytest

from controller.statistics import get_normal_pdf_axes, calculate_basic_stats
from numpy.random import randn


def test_calculate_basic_stats():
    mean, std = calculate_basic_stats(randn(100))
    assert mean == pytest.approx(0, abs=0.5)
    assert std == pytest.approx(1, rel=0.5)


def test_get_normal_pdf_axes():
    x, y = get_normal_pdf_axes(1, 10)

    assert len(x) == len(y)
