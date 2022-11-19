import pytest

from pathlib import Path

from model.data import (
    RawData,
    Data,
    refine_data,
    to_raw,
    load_raw_data,
    update_raw_data,
    update_json_file,
    read_column,
)


@pytest.fixture
def mock_folder() -> Path:
    return Path.cwd() / "tests/mock/"


@pytest.fixture
def right_raw_data() -> RawData:
    return RawData(
        **{
            "file": "test.xlsx",
            "column": "g (m/s^2)",
            "amount": "100",
            "bins": "7",
            "imgname": "histogram",
        }
    )


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


def test_refine_data(right_raw_data: RawData) -> None:
    data: Data = refine_data(right_raw_data)
    assert isinstance(data.file, Path)
    assert isinstance(data.amount, int)
    assert isinstance(data.bins, int)


def test_to_raw(right_data: Data) -> None:
    raw_data: RawData = to_raw
    for value in raw_data.__dict__.values():
        assert isinstance(value, str)


def test_load_raw_data(mock_folder: Path, right_raw_data: RawData) -> None:
    path: Path = mock_folder / "data.json"
    data: RawData = load_raw_data(path)
    assert data == right_raw_data

    path = mock_folder / "invalid_json.json"
    data = load_raw_data(path)
    assert data == RawData()

    path = mock_folder / "dont_exist.json"
    data = load_raw_data(path)
    assert data == RawData()


def test_fail_to_load_raw_data(mock_folder: Path) -> None:
    path: Path = mock_folder / "wrong_data.json"
    with pytest.raises(TypeError):
        load_raw_data(path)


def test_update_raw_data(mock_folder: Path) -> None:
    path: Path = mock_folder / "updatable_data.json"
    update_raw_data(path, RawData(imgname="updated"))

    with path.open() as file:
        for _ in range(5):
            file.readline()
        line: str = file.readline()

    assert line == '  "imgname": "updated"\n'

    update_raw_data(path, RawData())


def test_update_json_file(mock_folder: Path) -> None:
    path: Path = mock_folder / "updatable.json"

    update_json_file(path, {"update_me": 2})

    with path.open() as file:
        file.readline()
        line = file.readline()

    assert line == '  "update_me": 2\n'

    update_json_file(path, {"update_me": 1})


def test_read_column() -> None:
    path: Path = Path.cwd() / "test.xlsx"
    data = read_column(path, "a (m/s^2)")[:10]
    for value in data:
        assert round(value) == 10
