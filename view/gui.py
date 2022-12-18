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
        # self.page.on_resize = self.on_resize

        pick_files_dialog = ft.FilePicker(on_result=self.on_file_pick)
        pick_files = partial(
            pick_files_dialog.pick_files,
            initial_directory=Path.cwd().as_posix(),
            allow_multiple=False,
        )

        self.page.overlay.append(pick_files_dialog)

        text_input_style = {
            "border_radius": ft.border_radius.all(20),
            "border_color": ft.colors.BLACK12,
            "focused_border_color": ft.colors.PRIMARY,
        }

        input_section_title = ft.Column(
            controls=[
                ft.Text(
                    value="Set histogram info",
                    style=ft.TextThemeStyle.TITLE_LARGE,
                ),
                ft.Text(
                    value="Fill in the required histogram info",
                    style=ft.TextThemeStyle.BODY_SMALL,
                ),
            ],
            spacing=5,
        )

        self.file_name = ft.TextField(
            label="Choose a spreadsheet file",
            read_only=True,
            expand=True,
            **text_input_style,
        )
        pick_file = ft.Row(
            controls=[
                self.file_name,
                ft.IconButton(
                    icon=ft.icons.FILE_OPEN,
                    on_click=pick_files,
                    tooltip="Pick a file",
                    style=ft.ButtonStyle(
                        color=ft.colors.ON_PRIMARY,
                        bgcolor=ft.colors.PRIMARY,
                    ),
                ),
            ],
        )
        self.column_name = ft.Dropdown(
            label="Select a column",
            # prefix_icon=ft.icons.VIEW_COLUMN,
            **text_input_style,
        )
        self.amount = ft.TextField(
            label="Number of values to use",
            **text_input_style,
        )
        self.bins = ft.TextField(
            label="Number of bins",
            **text_input_style,
        )
        self.create_histogram_btn = ft.Container(
            content=ft.ElevatedButton(
                text="Create histogram",
                icon=ft.icons.BAR_CHART,
                style=ft.ButtonStyle(
                    color=ft.colors.ON_PRIMARY,
                    # color={
                    #     ft.MaterialState.HOVERED: ft.colors.WHITE,
                    #     # ft.MaterialState.FOCUSED: ft.colors.,
                    #     ft.MaterialState.DEFAULT: ft.colors.ON_PRIMARY,
                    # },
                    bgcolor=ft.colors.PRIMARY,
                    padding=ft.padding.all(20),
                ),
                on_click=self.create_histogram,
            ),
            # margin=ft.margin.only(top=50),
        )

        self.text_based_inputs = [
            self.column_name,
            self.amount,
            self.bins,
        ]

        input_section_content = ft.Column(
            controls=[
                input_section_title,
                ft.Divider(
                    color=ft.colors.BACKGROUND,
                    height=30,
                ),
                pick_file,
                self.column_name,
                self.amount,
                self.bins,
                ft.Divider(
                    color=ft.colors.BLACK12,
                    height=30,
                ),
                self.create_histogram_btn,
            ],
            spacing=15,
            expand=True,
        )

        chart_section_title = ft.Column(
            controls=[
                ft.Text(
                    value="Histogram chart",
                    style=ft.TextThemeStyle.TITLE_LARGE,
                ),
                ft.Text(
                    value="Visualization of the histogram chart",
                    style=ft.TextThemeStyle.BODY_SMALL,
                ),
            ],
            spacing=5,
        )
        self.chart = MatplotlibChart()
        chart_section = ft.Column(
            controls=[
                chart_section_title,
                ft.Divider(
                    color=ft.colors.BACKGROUND,
                    height=30,
                ),
                self.chart,
            ]
        )

        input_section = ft.Container(
            content=input_section_content,
            bgcolor=ft.colors.BACKGROUND,
            padding=ft.padding.all(30),
            border_radius=ft.border_radius.all(20),
            expand=True,
        )

        histogram_chart = ft.Container(
            content=chart_section,
            expand=True,
            bgcolor=ft.colors.BACKGROUND,
            border_radius=ft.border_radius.all(20),
            padding=ft.padding.all(30),
        )

        self.main_content = ft.Row(
            controls=[
                input_section,
                histogram_chart,
            ],
            spacing=20,
        )

        self.page.add(self.main_content)

    def on_resize(self, e: ControlEvent) -> None:
        inputs_height: float = (
            e.control.height - e.control.padding.bottom - e.control.padding.top
        )
        for control in self.main_content.controls:
            control.height = inputs_height

        print(f"{self.main_content.height = !r}")
        print(f"{e.control.height = !r}")

        self.page.update()

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
            file_name: str = self.data.spreadsheet_file.name
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
        for input_dialog in self.text_based_inputs:
            if not input_dialog.value:
                return None

        self.data.column = self.column_name.value
        self.data.amount = int(self.amount.value)
        self.data.bins = int(self.bins.value)

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
