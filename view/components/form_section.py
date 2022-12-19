from typing import Callable
from typing import Any

import flet as ft

TEXT_INPUT_STYLE = {
    "border_radius": ft.border_radius.all(20),
    "border_color": ft.colors.BLACK12,
    "focused_border_color": ft.colors.PRIMARY,
}


def init_file_name() -> ft.TextField:
    return ft.TextField(
        label="Choose a spreadsheet file",
        read_only=True,
        expand=True,
        **TEXT_INPUT_STYLE,
    )


def init_column_name() -> ft.Dropdown:
    return ft.Dropdown(
        label="Select a column",
        **TEXT_INPUT_STYLE,
    )


def init_number_of_values() -> ft.TextField:
    return ft.TextField(
        label="Number of values to use",
        **TEXT_INPUT_STYLE,
    )


def init_number_of_bins() -> ft.TextField:
    return ft.TextField(
        label="Number of bins",
        **TEXT_INPUT_STYLE,
    )


def init_create_histogram_btn(
    create_histogram_fn: Callable[[ft.ControlEvent], None],
) -> ft.Container:
    return ft.ElevatedButton(
        text="Create histogram",
        icon=ft.icons.BAR_CHART,
        style=ft.ButtonStyle(
            color=ft.colors.ON_PRIMARY,
            bgcolor=ft.colors.PRIMARY,
            padding=ft.padding.all(20),
        ),
        on_click=create_histogram_fn,
    )


def init_form_section(
    file_name: ft.TextField,
    pick_file: Callable[[Any], None],
    column_name: ft.Dropdown,
    number_of_values: ft.TextField,
    number_of_bins: ft.TextField,
    create_histogram_btn: ft.ElevatedButton,
) -> ft.Container:
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

    file_picker = ft.Row(
        controls=[
            file_name,
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
            column_name,
            number_of_values,
            number_of_bins,
            ft.Divider(
                color=ft.colors.BLACK12,
                height=30,
            ),
            create_histogram_btn,
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
