from pathlib import Path

from model.save import load


def test_fail_to_load() -> None:
    mock_file = Path("mock_file.picke")

    data = load(mock_file)
    assert data is None

    data = load(mock_file) or "mock_value"
    assert data == "mock_value"
