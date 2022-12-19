import pickle
from pathlib import Path

from .data import Data


def save(data: Data, filepath: Path) -> None:
    """
    Save current data.
    Serialize the Data object.
    """
    with open(filepath, "wb") as file:
        pickle.dump(data, file)


def load(filepath: Path) -> Data:
    """
    Load saved data.
    Deserialize the Data object.
    """
    if not filepath.exists():
        return Data()

    with open(filepath, "rb") as file:
        return pickle.load(file)
