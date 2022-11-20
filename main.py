import sys
from pathlib import Path
from functools import partial

from PyQt5.QtWidgets import QApplication

from view.gui import Window, init_app
from controller.plotting import create_hist
from controller.data_gen import norm_axes
from controller.data_process import get_stats
from model.data import read_column, read_data, save_data, Data

STYLESHEET: Path = Path.cwd() / "styles.css"
DATA_PATH: Path = Path.cwd() / "data.json"


def create_hist_fn(data: Data) -> None:
    """
    Gets the data object and provide the necessary arguments for the create
    histogram function.
    """
    hist_data: list[float] = read_column(data.file, data.column)[: data.amount]
    mean, std = get_stats(hist_data)
    lower_bound: int = min(hist_data)
    upper_bound: int = max(hist_data)
    x, y = norm_axes(start=lower_bound, end=upper_bound, mean=mean, std=std)

    create_hist(func_axes=(x, y), data=hist_data, bins=data.bins, filename=data.imgname)


def main() -> None:
    stylesheet: str = STYLESHEET.read_text()
    data: Data = read_data(DATA_PATH)
    save_data_fn = partial(save_data, DATA_PATH)

    with init_app(QApplication(sys.argv)):
        win = Window(
            data=data,
            stylesheet=stylesheet,
            create_hist_fn=create_hist_fn,
            save_data_fn=save_data_fn,
        )
        win.show()


if __name__ == "__main__":
    main()
