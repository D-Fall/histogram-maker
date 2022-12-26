from pathlib import Path

from pandas import read_excel, DataFrame


def get_data_frame(filepath: Path) -> DataFrame:
    """Read data frame."""
    assert isinstance(filepath, Path)
    assert filepath.exists()

    return read_excel(filepath)
