from pathlib import Path

import pytest

from controller.spreadsheet import get_data_frame


def test_fail_to_get_data_frame():
    with pytest.raises(AssertionError):
        get_data_frame(Path("mock_spreadsheet.xlsx"))

    with pytest.raises(AssertionError):
        get_data_frame("mock_spreadsheet.xlsx")
