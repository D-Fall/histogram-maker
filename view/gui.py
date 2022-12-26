"""
Expected behaviour

Enter without any data:
    - Only file picker is visible
    - The create histogram button is disabled

    Pick file:
        - Show hidden inputs
        - All inputs are empty
        - Enable the create histogram button
        - Create the column name dropdown options

        Clicked the create histogram button:
            - Only work if all the inputs are filled
            - Save the current data

Enter with data:
    - Load the existing data
    - Create the column name dropdown options
    - Everything is visible and filled
    - Create histogram button should work out of the box

    Picked another file:
        - Update the column name dropdown options
"""

from functools import partial
from pathlib import Path
from typing import Callable
from itertools import islice

import flet as ft
from flet.file_picker import FilePickerFile

from matplotlib.figure import Figure

from controller.spreadsheet import get_data_frame
from model.data import Data
from .components.chart_section import ChartSection
from .components.form_section import FormSection


class App:
    def __init__(
        self,
        page: ft.Page,
        data: Data,
        create_histogram_fn: Callable[[Data], Figure],
        save_path: Path,
    ):
        self.page = page
        self.data = data
        self.create_histogram_fn = create_histogram_fn
        self.save_path = save_path

        self.init_ui()
        self.update_input_fields()

    def on_resize(self, e: ft.ControlEvent):
        print(f"{e.control.height = }")
        print(f"{e.control.width = }")

    def init_ui(self):
        self.page.title = "The Histogram Maker"
        self.page.padding = ft.padding.all(20)
        self.page.bgcolor = ft.colors.PRIMARY_CONTAINER
        self.page.scroll = ft.ScrollMode.AUTO
        self.page.on_resize = self.on_resize

        self.form_section = FormSection(col={"md": 12, "lg": 6})
        self.form_section.pick_files_dialog.on_result = (
            self.on_file_pick_result
        )
        self.form_section.create_histogram_btn.on_click = self.create_histogram

        self.page.overlay.append(self.form_section.pick_files_dialog)

        self.input_fields = self.form_section.get_input_fields()

        self.chart_section = ChartSection(col={"md": 12, "lg": 6})

        main_content = ft.ResponsiveRow(
            controls=[
                self.form_section,
                self.chart_section,
            ],
            spacing=20,
        )

        self.page.add(main_content)

    def hide_inputs(self):
        """
        Hide the input fields except the file picker and disable the
        create histogram button.
        """
        for input_field in islice(self.input_fields.values(), 1, None):
            input_field.visible = False

        self.form_section.create_histogram_btn.disabled = True

        self.form_section.update()

    def show_inputs(self):
        """
        Show the hidden input fields and enable the create histogram
        button.
        """
        for input_field in islice(self.input_fields.values(), 1, None):
            input_field.visible = True

        self.form_section.create_histogram_btn.disabled = False

        self.form_section.update()

    def fill_inputs(self):
        """Fill in the input fields with the existing data."""
        file_name: str = self.data.spreadsheet_file.name
        self.form_section.file_name.value = file_name

        for field_name in islice(self.input_fields, 1, None):
            self.input_fields[field_name].value = str(
                self.data.__dict__[field_name]
            )

        self.form_section.update()

    def set_column_name_options(self):
        data_frame = get_data_frame(self.data.spreadsheet_file)
        options = [
            ft.dropdown.Option(column_name) for column_name in data_frame
        ]
        self.form_section.column_name.options = options

    def update_input_fields(self):
        """Hide or fill the input fields based of the existance of data."""
        if self.data == Data():
            self.hide_inputs()
        else:
            self.set_column_name_options()
            self.fill_inputs()

    def on_file_pick_result(self, e: ft.FilePickerResultEvent):
        """
        Responsible for update the column name dropdown menu and the
        file name that appears on the file name field. It also shows the
        hidden input fields.
        """
        if e.files:
            file: FilePickerFile = e.files[0]
            self.form_section.file_name.value = file.name
            self.data.spreadsheet_file = Path(file.path)

            self.set_column_name_options()

            self.show_inputs()

    def update_data(self) -> bool:
        """
        Update the data object if all fields are properly filled.

        Returns a status ok:
            - True if all went well
            - False if there is a field missing
        """
        for input_dialog in self.input_fields.values():
            if input_dialog.value is None:
                return False

        for field_name, input_field in islice(
            self.input_fields.items(), 1, None
        ):
            value: str = str(input_field.value)
            if value.isdigit():
                self.data.__dict__[field_name] = int(value)
            else:
                self.data.__dict__[field_name] = input_field.value

        return True

    def create_histogram(self, e: ft.ControlEvent):
        """
        If the data is properly filled, updates the data object, creates
        the figure and sets the chart to that figure. Then save the data
        and update the chart section.

        If the data is not properly filled, it does nothing.
        """
        status_ok = self.update_data()
        if not status_ok:
            return None

        fig: Figure = self.create_histogram_fn(self.data)
        self.chart_section.chart.figure = fig

        self.data.save(self.save_path)

        self.chart_section.update()


def run_app(
    data: Data,
    create_histogram_fn: Callable[[Data], Figure],
    save_path: Path,
):
    def init_app(
        page: ft.Page,
        data: Data,
        create_histogram_fn: Callable[[Data], Figure],
        save_path: Path,
    ):
        App(
            page=page,
            data=data,
            create_histogram_fn=create_histogram_fn,
            save_path=save_path,
        )

    init_ui = partial(
        init_app,
        data=data,
        create_histogram_fn=create_histogram_fn,
        save_path=save_path,
    )

    ft.app(target=init_ui)
