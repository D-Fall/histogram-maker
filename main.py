from pathlib import Path
from functools import partial

from matplotlib.figure import Figure

from view.gui import run_app
from controller.plotting import create_histogram
from controller.statistics import calculate_basic_stats, get_normal_pdf_axes
from model.data import Data
from model.spreadsheet import get_data_frame
from model.save import load, save

DATA_PATH: Path = Path.cwd() / "data.pickle"


def create_histogram_fn(data: Data) -> Figure:
    """
    Gets the data object and provide the necessary arguments for the create
    histogram function.
    """
    data_frame = get_data_frame(data.spreadsheet_file)
    histogram_data: list[float] = data_frame[data.column][: data.amount]
    mean, std = calculate_basic_stats(histogram_data)
    lower_bound: int = min(histogram_data)
    upper_bound: int = max(histogram_data)
    x, y = get_normal_pdf_axes(start=lower_bound, end=upper_bound, mean=mean, std=std)

    return create_histogram(func_axes=(x, y), data=histogram_data, bins=data.bins)


def main() -> None:
    data: Data = load(DATA_PATH)
    save_data_fn = partial(save, filepath=DATA_PATH)

    run_app(
        data=data,
        create_histogram_fn=create_histogram_fn,
        save_data_fn=save_data_fn,
    )


if __name__ == "__main__":
    main()
