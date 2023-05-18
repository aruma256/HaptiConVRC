import flet as ft


LICENSE_TEXT = r"""
{PLACEHOLDER}
"""


class OSSLicenseView(ft.View):
    def __init__(self, page: ft.Page):
        super().__init__(
            route="/osslicense",
            controls=[
                ft.AppBar(
                    title=ft.Text("OSS License"),
                    bgcolor=ft.colors.SURFACE_VARIANT,
                ),
                ft.Text(
                    LICENSE_TEXT,
                )
            ],
        )
        self.scroll = "always"
