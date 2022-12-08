from pathlib import Path
from dataclasses import dataclass


@dataclass
class Data:
    spreadsheet_file: Path
    column: str
    amount: int
    bins: int
