import json
from pathlib import Path

from config.data import Data


def load_json(filepath: str) -> dict:
    try:
        with open(filepath, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {
            "file": "",
            "column": "",
            "data": "",
            "bins": "",
            "imgname": "histogram",
        }
    except json.JSONDecodeError:
        return {
            "file": "",
            "column": "",
            "data": "",
            "bins": "",
            "imgname": "histogram",
        }


def update_file(filepath: str, data: dict) -> None:
    with open(filepath, "w") as f:
        json.dump(data, f, indent=2)


def update_data(filepath: Path, data: Data) -> None:
    with open(filepath, "w") as data_file:
        json.dump(data.__dict__, data_file, indent=2)
