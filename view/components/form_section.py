from functools import partial
from pathlib import Path

import flet as ft


class FormSection(ft.UserControl):
    """
    Section that contains all the user inputs controls necessary to produce the
    histogram.

    There are some methods that have to be defined after the creation of the
    FormSection object because they require data acess. They are:
        - create_histogram_btn.on_click
        - pick_files_dialog.on_result
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        common_input_style = {
            "border_radius": ft.border_radius.all(20),
            "border_color": ft.colors.BLACK12,
            "focused_border_color": ft.colors.PRIMARY,
        }

        self.file_name = ft.TextField(
            label="Choose a spreadsheet file",
            read_only=True,
            expand=True,
            **common_input_style,
        )

        self.column_name = ft.Dropdown(
            label="Select a column",
            **common_input_style,
        )

        self.number_of_values = ft.TextField(
            label="Number of values to use",
            **common_input_style,
        )

        self.number_of_bins = ft.TextField(
            label="Number of bins",
            **common_input_style,
        )

        self.create_histogram_btn = ft.ElevatedButton(
            text="Create histogram",
            icon=ft.icons.BAR_CHART,
            style=ft.ButtonStyle(
                color=ft.colors.ON_PRIMARY,
                bgcolor=ft.colors.PRIMARY,
                padding=ft.padding.all(20),
            ),
        )

        self.pick_files_dialog = ft.FilePicker()

        self.input_fields: dict[str, ft.TextField | ft.Dropdown] = {
            "file_name": self.file_name,
            "column_name": self.column_name,
            "number_of_values": self.number_of_values,
            "number_of_bins": self.number_of_bins,
        }

    def build(self) -> ft.Container:
        title = ft.Column(
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

        pick_file = partial(
            self.pick_files_dialog.pick_files,
            initial_directory=Path.cwd().as_posix(),
            allow_multiple=False,
        )

        file_picker = ft.Row(
            controls=[
                self.file_name,
                ft.IconButton(
                    icon=ft.icons.FILE_OPEN,
                    on_click=pick_file,
                    tooltip="Pick a file",
                    style=ft.ButtonStyle(
                        color=ft.colors.ON_PRIMARY,
                        bgcolor=ft.colors.PRIMARY,
                    ),
                ),
            ],
        )

        form_content = ft.Column(
            controls=[
                title,
                ft.Divider(
                    color=ft.colors.BACKGROUND,
                    height=30,
                ),
                file_picker,
                self.column_name,
                self.number_of_values,
                self.number_of_bins,
                ft.Divider(
                    color=ft.colors.BLACK12,
                    height=30,
                ),
                self.create_histogram_btn,
            ],
            spacing=15,
            expand=True,
        )

        return ft.Container(
            content=form_content,
            bgcolor=ft.colors.BACKGROUND,
            padding=ft.padding.all(30),
            border_radius=ft.border_radius.all(20),
            expand=True,
        )
