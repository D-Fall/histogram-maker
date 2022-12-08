from pathlib import Path

import pytest

from model.spreadsheet import get_data_frame


def test_fail_to_get_data_frame() -> None:
    with pytest.raises(AssertionError):
        get_data_frame(Path("mock_spreadsheet.xlsx"))

    with pytest.raises(AssertionError):
        get_data_frame("mock_spreadsheet.xlsx")
