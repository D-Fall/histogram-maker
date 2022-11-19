import json
from dataclasses import dataclass
from pathlib import Path

from pandas import read_excel, DataFrame, Series


@dataclass
class RawData:
    file: str = ""
    column: str = ""
    amount: str = ""
    bins: str = ""
    imgname: str = "histogram"


@dataclass
class Data:
    file: Path
    column: str
    amount: int
    bins: int
    imgname: str


def refine_data(data: RawData) -> Data:
    return Data(
        file=Path.cwd() / data.file,
        column=data.column,
        amount=int(data.amount),
        bins=int(data.bins),
        imgname=data.imgname,
    )


def to_raw(data: Data) -> RawData:
    raw_data = {}
    for name, value in data.__dict__.items():
        raw_data[name] = str(value)

    return RawData(**raw_data)


def load_raw_data(filepath: Path) -> Data:
    try:
        with open(filepath, "r") as data_file:
            data: dict[str, str] = json.load(data_file)
            return RawData(**data)
    except FileNotFoundError:
        return RawData()
    except json.JSONDecodeError:
        return RawData()


def update_json_file(filepath: Path, data: dict) -> None:
    with open(filepath, "w") as json_file:
        json.dump(data, json_file, indent=2)


def update_raw_data(filepath: Path, data: RawData) -> None:
    with open(filepath, "w") as data_file:
        json.dump(data.__dict__, data_file, indent=2)


def read_column(filepath: Path, column: str) -> Series:
    data_frame: DataFrame = read_excel(filepath)
    return data_frame[column]
