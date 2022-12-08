import json
from dataclasses import dataclass
from pathlib import Path

from pandas import read_excel, DataFrame

DataDict = dict[str, Path | str | int]


@dataclass
class Data:
    file: Path = Path.cwd()
    column: str = ""
    amount: int = 0
    bins: int = 0
    imgname: str = ""


def read_data(filepath: Path) -> Data:
    """
    Reads the data json file and make it available to the code in the form of a
    Data class.

    In the case of any exceptions, it returns a template with the default values
    of each field.
    """
    try:
        with open(filepath, "r") as data_file:
            data: DataDict = json.load(data_file)
            data["file"] = Path.cwd() / data["file"]
            return Data(**data)
    except FileNotFoundError:
        return Data()
    except json.JSONDecodeError:
        return Data()


def save_data(filepath: Path, data: Data) -> None:
    """
    Reads a Data object and saves it to a data json file.

    Path objects cannot be saved in json, so only the name of the file, if
    exists, is stored.
    """
    data_d: DataDict = data.__dict__
    data_d["file"] = data.file.name if data.file != Path.cwd() else ""

    with open(filepath, "w") as data_file:
        json.dump(data_d, data_file, indent=2)


def read_column(filepath: Path, column: str) -> list[float]:
    """
    Uses pandas to read a spreadsheet file (.xlsx, .xls) and return the data
    from a column.

    The actual return type is pd.Serial, but it can be treated just like an list
    of floats.
    """
    data_frame: DataFrame = read_excel(filepath)
    return data_frame[column]
