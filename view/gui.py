from functools import partial
from pathlib import Path
from typing import Callable

import flet as ft
from flet.matplotlib_chart import MatplotlibChart
from flet.file_picker import FilePickerFile
from matplotlib.figure import Figure

from model.spreadsheet import get_data_frame
from model.data import Data


class App:
    def __init__(
        self,
        page: ft.Page,
        data: Data,
        create_histogram_fn: Callable[[Data], Figure],
        save_data_fn: Callable[[Data], None],
    ):
        self.page = page
        self.data = data
        self.create_histogram_fn = create_histogram_fn
        self.save_data_fn = save_data_fn

        self.init_ui()
        self.load_data()

    def init_ui(self):
        pick_files_dialog = ft.FilePicker(on_result=self.on_file_pick)
        pick_files = partial(
            pick_files_dialog.pick_files,
            initial_directory=Path.cwd().as_posix(),
            allow_multiple=False,
        )

        self.page.overlay.append(pick_files_dialog)

        self.file_name = ft.Text()
        self.pick_file = ft.ElevatedButton(
            text="Pick spreadsheet file",
            icon=ft.icons.FILE_OPEN,
            on_click=pick_files,
        )
        self.column_name = ft.Dropdown(label="Column")
        self.amount = ft.TextField(label="Amount of data")
        self.bins = ft.TextField(label="Amount of bins")
        self.create_histogram_btn = ft.ElevatedButton(
            text="Create histogram",
            icon=ft.icons.BAR_CHART,
            on_click=self.create_histogram,
        )

        self.inputs = ft.Column(
            controls=[
                self.file_name,
                self.pick_file,
                self.column_name,
                self.amount,
                self.bins,
                self.create_histogram_btn,
            ],
        )

        self.chart = MatplotlibChart(expand=True)

        main_content = ft.Row(
            controls=[
                self.inputs,
                self.chart,
            ]
        )

        background = ft.Container(content=main_content)

        self.page.add(background)

    def load_data(self) -> None:
        if self.data is None:
            self.file_name.value = "No file selected."
            self.column_name.visible = False

            self.data = Data(
                spreadsheet_file=Path(""),
                column="",
                amount=0,
                bins=0,
            )

            self.page.update()
        else:
            file_name = self.data.spreadsheet_file.name
            self.file_name.value = file_name

            data_frame = get_data_frame(self.data.spreadsheet_file)
            options = [ft.dropdown.Option(column_name) for column_name in data_frame]

            self.column_name.visible = True
            self.column_name.options = options
            self.column_name.value = self.data.column

            self.amount.value = self.data.amount or ""
            self.bins.value = self.data.bins or ""

            self.page.update()

    def on_file_pick(self, e: ft.FilePickerResultEvent) -> None:
        if e.files:
            file: FilePickerFile = e.files[0]
            self.file_name.value = file.name
            self.data.spreadsheet_file = Path(file.path)

            self.load_data()

            self.page.update()

    def update_data(self) -> None:
        for input_dialog in self.inputs.controls[1:]:
            if isinstance(input_dialog, ft.ElevatedButton):
                print(f"{input_dialog} is a button")
                continue

            if not input_dialog.value:
                print(f"no value in {input_dialog}")
                return None

        self.data.column = self.column_name.value
        self.data.amount = int(self.amount.value)
        self.data.bins = int(self.bins.value)

    def create_histogram(self, e) -> None:
        self.update_data()
        if self.data is None:
            return None

        fig: Figure = self.create_histogram_fn(self.data)
        self.chart.figure = fig

        self.save_data_fn(self.data)

        self.page.update()


def run_app(
    data: Data,
    create_histogram_fn: Callable[[Data], Figure],
    save_data_fn: Callable[[Data], None],
) -> None:
    def init_app(
        page: ft.Page,
        data: Data,
        create_histogram_fn: Callable[[Data], Figure],
        save_data_fn: Callable[[Data], None],
    ) -> None:
        App(
            page=page,
            data=data,
            create_histogram_fn=create_histogram_fn,
            save_data_fn=save_data_fn,
        )

    init_ui = partial(
        init_app,
        data=data,
        create_histogram_fn=create_histogram_fn,
        save_data_fn=save_data_fn,
    )

    ft.app(target=init_ui)
