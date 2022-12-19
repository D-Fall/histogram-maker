from pathlib import Path
from dataclasses import dataclass


@dataclass
class Data:
    spreadsheet_file: Path = Path()
    column_name: str = ""
    number_of_values: int = 0
    number_of_bins: int = 0
