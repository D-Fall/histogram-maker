import json
from dataclasses import dataclass
from pathlib import Path

from pandas import read_excel, DataFrame, Series


@dataclass
class Data:
    file: Path = ""
    column: str = ""
    amount: int = ""
    bins: int = ""
    imgname: str = "histogram"


def load_json_data(filepath: Path) -> Data:
    try:
        with open(filepath, "r") as data_file:
            data: dict[str, str] = json.load(data_file)
            return Data(**data)
    except FileNotFoundError:
        return Data()
    except json.JSONDecodeError:
        return Data()


def update_json_file(filepath: Path, data: dict) -> None:
    with open(filepath, "w") as json_file:
        json.dump(data, json_file, indent=2)


def update_json_data(filepath: Path, data: Data) -> None:
    with open(filepath, "w") as data_file:
        json.dump(data.__dict__, data_file, indent=2)


def read_spreadsheet(filepath: Path, column: str, limit: int) -> Series:
    data_frame: DataFrame = read_excel(filepath)
    return data_frame[column][:limit]
