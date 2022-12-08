from pathlib import Path
from dataclasses import dataclass


@dataclass
class Data:
    file: Path
    column: str
    amount: int
    bins: int
    imgname: str
