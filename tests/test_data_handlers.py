import pytest

from pathlib import Path

from model.data_handle import (
    Data,
    read_data,
    save_data,
    read_column,
)


@pytest.fixture
def mock_folder() -> Path:
    return Path.cwd() / "tests/mock/"


@pytest.fixture
def right_data() -> Data:
    return Data(
        **{
            "file": Path.cwd() / "test.xlsx",
            "column": "g (m/s^2)",
            "amount": 100,
            "bins": 7,
            "imgname": "histogram",
        }
    )


def test_read_data(mock_folder: Path, right_data: Data) -> None:
    path: Path = mock_folder / "data.json"
    data: Data = read_data(path)
    assert data == right_data

    path = mock_folder / "invalid_json.json"
    data = read_data(path)
    assert data == Data()

    path = mock_folder / "dont_exist.json"
    data = read_data(path)
    assert data == Data()


def test_fail_to_read_data(mock_folder: Path) -> None:
    path: Path = mock_folder / "wrong_data.json"
    with pytest.raises(TypeError):
        read_data(path)


def test_save_data(mock_folder: Path) -> None:
    path: Path = mock_folder / "updatable_data.json"
    save_data(path, Data(imgname="updated"))

    with path.open() as file:
        for _ in range(5):
            file.readline()
        line: str = file.readline()

    assert line == '  "imgname": "updated"\n'

    save_data(path, Data())


def test_read_column() -> None:
    path: Path = Path.cwd() / "test.xlsx"
    data = read_column(path, "a (m/s^2)")[:10]
    for value in data:
        assert round(value) == 10
