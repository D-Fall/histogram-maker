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
from flet.matplotlib_chart import MatplotlibChart
from flet.file_picker import FilePickerFile

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
        self.update_input_fields()

    def on_resize(self, e: ft.ControlEvent) -> None:
        print(f"{e.control.height = }")
        print(f"{e.control.width = }")

    def init_ui(self):
        self.page.title = "The Histogram Maker"
        self.page.padding = ft.padding.all(20)
        self.page.bgcolor = ft.colors.PRIMARY_CONTAINER
        self.page.scroll = ft.ScrollMode.AUTO
        self.page.on_resize = self.on_resize

        pick_files_dialog = ft.FilePicker(on_result=self.on_file_pick_result)
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

        self.form_inputs: dict[str, ft.TextField | ft.Dropdown] = {
            "file_name": self.file_name,
            "column_name": self.column_name,
            "number_of_values": self.number_of_values,
            "number_of_bins": self.number_of_bins,
        }

        self.form_section = init_form_section(
            file_name=self.file_name,
            pick_file=pick_file,
            column_name=self.column_name,
            number_of_values=self.number_of_values,
            number_of_bins=self.number_of_bins,
            create_histogram_btn=self.create_histogram_btn,
        )

        self.chart = MatplotlibChart()

        self.chart_section = init_chart_section(chart=self.chart)

        main_content = ft.Row(
            controls=[
                self.form_section,
                self.chart_section,
            ],
            spacing=20,
        )

        self.page.add(main_content)

    def hide_inputs(self) -> None:
        """
        Hide the input fields except the file picker and disable the create
        histogram button.
        """
        for input_field in islice(self.form_inputs.values(), 1, None):
            input_field.visible = False

        self.create_histogram_btn.disabled = True

        self.form_section.update()

    def show_inputs(self) -> None:
        """
        Show the hidden input fields and enable the create histogram button.
        """
        for input_field in islice(self.form_inputs.values(), 1, None):
            input_field.visible = True

        self.create_histogram_btn.disabled = False

        self.form_section.update()

    def fill_inputs(self) -> None:
        """
        Fill in the input fields with the existing data.
        """
        file_name: str = self.data.spreadsheet_file.name
        self.file_name.value = file_name

        for field_name in islice(self.form_inputs, 1, None):
            self.form_inputs[field_name].value = str(self.data.__dict__[field_name])

        self.form_section.update()

    def set_column_name_options(self) -> None:
        data_frame = get_data_frame(self.data.spreadsheet_file)
        options = [ft.dropdown.Option(column_name) for column_name in data_frame]
        self.column_name.options = options

    def update_input_fields(self) -> None:
        """
        Hide or fill the input fields based of the existance of data.
        """
        if self.data == Data():
            self.hide_inputs()
        else:
            self.set_column_name_options()
            self.fill_inputs()

    def on_file_pick_result(self, e: ft.FilePickerResultEvent) -> None:
        """
        Responsible for update the column name dropdown menu and the file name
        that appears on the file name field. It also shows the hidden input
        fields.
        """
        if e.files:
            file: FilePickerFile = e.files[0]
            self.file_name.value = file.name
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
        for input_dialog in self.form_inputs.values():
            if input_dialog.value is None:
                return False

        for field_name in islice(self.form_inputs, 1, None):
            input_value: str = self.form_inputs[field_name].value
            print(type(input_value))
            if input_value.isdigit():
                self.data.__dict__[field_name] = int(input_value)
            else:
                self.data.__dict__[field_name] = input_value

        return True

    def create_histogram(self, e: ft.ControlEvent) -> None:
        """
        If the data is properly filled, updates the data object, creates the
        figure and sets the chart to that figure. Then save the data and update
        the chart section.

        If the data is not properly filled, it does nothing.
        """
        status_ok = self.update_data()
        if not status_ok:
            return None

        fig: Figure = self.create_histogram_fn(self.data)
        self.chart.figure = fig

        self.save_data_fn(self.data)

        self.chart_section.update()


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
