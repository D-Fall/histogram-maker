from __future__ import annotations

import pickle
from pathlib import Path
from dataclasses import dataclass


@dataclass
class Data:
    spreadsheet_file: Path = Path()
    column_name: str = ""
    number_of_values: int = 0
    number_of_bins: int = 0

    def save(self, filepath: Path):
        """
        Save current data.
        Serialize the Data object.
        """
        with open(filepath, "wb") as file:
            pickle.dump(self, file)

    @classmethod
    def load(cls, filepath: Path) -> Data:
        """
        Load saved data.
        Deserialize the Data object.
        """
        if not filepath.exists():
            return cls()

        with open(filepath, "rb") as file:
            return pickle.load(file)
