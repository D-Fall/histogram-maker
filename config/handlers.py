import json
from pathlib import Path

from config.data import Data
from config import DATA_TEMPLATE


def load_data_file(filepath: Path) -> Data:
    try:
        with open(filepath, "r") as data_file:
            data = json.load(data_file)
            return Data(
                file=data["file"],
                column=data["column"],
                amount=data["amount"],
                bins=data["bins"],
                imgname=data["imgname"],
            )
    except FileNotFoundError:
        return DATA_TEMPLATE
    except json.JSONDecodeError:
        return DATA_TEMPLATE


def update_file(filepath: str, data: dict) -> None:
    with open(filepath, "w") as f:
        json.dump(data, f, indent=2)


def update_data_file(filepath: Path, data: Data) -> None:
    with open(filepath, "w") as data_file:
        json.dump(data.__dict__, data_file, indent=2)
