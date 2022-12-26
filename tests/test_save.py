from pathlib import Path

import pytest

from model.data import Data


@pytest.fixture
def filepath() -> Path:
    return Path.cwd() / "tests/mock/test_data.pickle"


@pytest.fixture
def data() -> Data:
    return Data(
        spreadsheet_file=Path.cwd(),
        column_name="mock column name",
        number_of_values=3,
        number_of_bins=3,
    )


def test_save(filepath: Path, data: Data):
    if filepath.exists():
        filepath.unlink()

    data.save(filepath)

    assert filepath.exists()


def test_load(filepath: Path, data: Data):
    loaded_data = Data.load(filepath)

    assert loaded_data == data


def test_fail_to_load():
    mock_file = Path("mock_file.picke")

    mock_data = Data.load(mock_file)
    assert mock_data == Data()
