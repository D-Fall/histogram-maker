import pytest

from pathlib import Path

from model.data import (
    Data,
    load_json_data,
    update_json_data,
    update_json_file,
    read_spreadsheet,
)


@pytest.fixture
def mock_folder() -> Path:
    return Path.cwd() / "tests/mock/"


@pytest.fixture
def right_data() -> Data:
    return Data(
        **{
            "file": "test.xlsx",
            "column": "g (m/s^2)",
            "amount": "100",
            "bins": "7",
            "imgname": "histogram",
        }
    )


def test_load_json_data(mock_folder: Path, right_data: Data) -> None:
    path: Path = mock_folder / "data.json"
    data: Data = load_json_data(path)
    assert data == right_data

    path = mock_folder / "invalid_json.json"
    data = load_json_data(path)
    assert data == Data()

    path = mock_folder / "dont_exist.json"
    data = load_json_data(path)
    assert data == Data()


def test_fail_to_load_json_data(mock_folder: Path) -> None:
    path: Path = mock_folder / "wrong_data.json"
    with pytest.raises(TypeError):
        load_json_data(path)


def test_update_json_data(mock_folder: Path) -> None:
    path: Path = mock_folder / "updatable_data.json"
    update_json_data(path, Data(imgname="updated"))

    with path.open() as file:
        for _ in range(5):
            file.readline()
        line: str = file.readline()

    assert line == '  "imgname": "updated"\n'

    update_json_data(path, Data())


def test_update_json_file(mock_folder: Path) -> None:
    path: Path = mock_folder / "updatable.json"

    update_json_file(path, {"update_me": 2})

    with path.open() as file:
        file.readline()
        line = file.readline()

    assert line == '  "update_me": 2\n'

    update_json_file(path, {"update_me": 1})


def test_read_spreadsheet() -> None:
    path: Path = Path.cwd() / "test.xlsx"
    data = read_spreadsheet(path, "a (m/s^2)", 10)
    for value in data:
        assert round(value) == 10
