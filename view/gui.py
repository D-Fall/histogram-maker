from functools import partial
from pathlib import Path
from typing import Callable

import flet as ft
from flet.matplotlib_chart import MatplotlibChart
from flet.file_picker import FilePickerFile
from flet.control_event import ControlEvent

from matplotlib.figure import Figure

from model.spreadsheet import get_data_frame
from model.data import Data
from .components.chart_section import init_chart_section
from .components.form_section import (
    init_file_name,
    init_column_name,
    init_number_of_values,
    init_number_of_bins,
    init_create_histogram_btn,
    init_form_section,
)


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
        self.page.padding = ft.padding.all(20)
        self.page.bgcolor = ft.colors.PRIMARY_CONTAINER

        pick_files_dialog = ft.FilePicker(on_result=self.on_file_pick)
        pick_file = partial(
            pick_files_dialog.pick_files,
            initial_directory=Path.cwd().as_posix(),
            allow_multiple=False,
        )

        self.page.overlay.append(pick_files_dialog)

        self.file_name: ft.TextField = init_file_name()
        self.column_name: ft.Dropdown = init_column_name()
        self.number_of_values: ft.TextField = init_number_of_values()
        self.number_of_bins: ft.TextField = init_number_of_bins()
        self.create_histogram_btn: ft.ElevatedButton = init_create_histogram_btn(
            create_histogram_fn=self.create_histogram,
        )

        self.form_inputs = [
            self.file_name,
            self.column_name,
            self.number_of_values,
            self.number_of_bins,
        ]

        form_section = init_form_section(
            file_name=self.file_name,
            pick_file=pick_file,
            column_name=self.column_name,
            number_of_values=self.number_of_values,
            number_of_bins=self.number_of_bins,
            create_histogram_btn=self.create_histogram_btn,
        )

        self.chart = MatplotlibChart()

        chart_section = init_chart_section(chart=self.chart)

        main_content = ft.Row(
            controls=[
                form_section,
                chart_section,
            ],
            spacing=20,
        )

        self.page.add(main_content)

    def load_data(self) -> None:
        """ """
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
            file_name: str = self.data.spreadsheet_file.name
            self.file_name.value = file_name

            data_frame = get_data_frame(self.data.spreadsheet_file)
            options = [ft.dropdown.Option(column_name) for column_name in data_frame]

            self.column_name.visible = True
            self.column_name.options = options
            self.column_name.value = self.data.column

            self.number_of_values.value = self.data.amount or ""
            self.number_of_bins.value = self.data.bins or ""

            self.page.update()

    def on_file_pick(self, e: ft.FilePickerResultEvent) -> None:
        if e.files:
            file: FilePickerFile = e.files[0]
            self.file_name.value = file.name
            self.data.spreadsheet_file = Path(file.path)

            self.load_data()

            self.page.update()

    def update_data(self) -> None:
        for input_dialog in self.form_inputs:
            if not input_dialog.value:
                return None

        self.data.column = self.column_name.value
        self.data.amount = int(self.number_of_values.value)
        self.data.bins = int(self.number_of_bins.value)

    def create_histogram(self, e: ControlEvent) -> None:
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
