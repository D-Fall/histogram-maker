from controller.data_gen import norm_axes


def test_norm_axes() -> None:
    x, y = norm_axes(1, 10)

    assert len(x) == len(y)
