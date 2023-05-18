import flet as ft

from .core import Core

VERSION = "0.3.0"
APP_TITLE = f"HaptiConVRC v{VERSION}"
LICENSE_TEXT = r"""
{PLACEHOLDER}
"""


class App:
    def main(self, page: ft.Page):
        page.title = APP_TITLE
        self._core = Core()
        self._core.start_osc_server()

        self._app_bar = ft.AppBar(
            title=ft.Text(APP_TITLE),
            bgcolor=ft.colors.SURFACE_VARIANT,
        )
        self._position_text = ft.Text()
        self._connect_l_button = ft.ElevatedButton(
            "コントローラー L を接続する",
            on_click=self._connect_l_button_clicked,
        )
        self._connect_r_button = ft.ElevatedButton(
            "コントローラー R を接続する",
            on_click=self._connect_r_button_clicked,
        )
        self._oss_button = ft.ElevatedButton(
            "OSSライセンス",
            on_click=self._show_oss_license,
        )
        page.controls.extend(
            [
                self._app_bar,
                self._connect_l_button,
                self._connect_r_button,
                self._position_text,
                self._oss_button,
            ],
        )
        page.update()

    def _connect_l_button_clicked(self, event):
        try:
            self._core.connect_controller("L")
        except OSError:
            dialog = ft.AlertDialog(
                title=ft.Text("コントローラー L を接続できませんでした")
            )
            event.page.dialog = dialog
            dialog.open = True
            event.page.update()

    def _connect_r_button_clicked(self, event):
        try:
            self._core.connect_controller("R")
        except OSError:
            dialog = ft.AlertDialog(
                title=ft.Text("コントローラー R を接続できませんでした")
            )
            event.page.dialog = dialog
            dialog.open = True
            event.page.update()

    def _show_oss_license(self, event):
        dialog = ft.AlertDialog(
            title=ft.Text("OSSライセンス"),
            content=ft.Column([ft.Text(LICENSE_TEXT)], scroll="always"),
        )
        event.page.dialog = dialog
        dialog.open = True
        event.page.update()

    def on_position_updated(self, position):
        self._position_text.value = str(position)
        self.page.update()


def start():
    app = App()
    ft.app(target=app.main)
