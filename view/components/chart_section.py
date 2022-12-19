import flet as ft
from flet.matplotlib_chart import MatplotlibChart


def init_chart_section(chart: MatplotlibChart) -> ft.Container:
    title = ft.Column(
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

    chart_content = ft.Column(
        controls=[
            title,
            ft.Divider(
                color=ft.colors.BACKGROUND,
                height=30,
            ),
            chart,
        ]
    )

    return ft.Container(
        content=chart_content,
        expand=True,
        bgcolor=ft.colors.BACKGROUND,
        border_radius=ft.border_radius.all(20),
        padding=ft.padding.all(30),
        col={"md": 12, "lg": 6},
    )
