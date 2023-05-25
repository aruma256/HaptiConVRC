import flet as ft

from .core import Core
from .version_checker import VersionChecker

VERSION = "0.3.0"
APP_TITLE = f"HaptiConVRC v{VERSION}"
LICENSE_TEXT = r"""
{PLACEHOLDER}
"""
DOWNLOAD_LINK = "https://github.com/aruma256/HaptiConVRC/wiki/Download"
WINDOW_WIDTH = 600


class App:
    def __init__(self) -> None:
        self.core = Core()

    def main(self, page: ft.Page):
        page.title = APP_TITLE
        page.window_width = WINDOW_WIDTH

        self.core.start_osc_server()

        def rumble_level_l_on_start_slider_callback(event):
            self.core.rumble_config.l_level_on_start = int(event.control.value)

        def rumble_level_l_on_move_max_slider_callback(event):
            self.core.rumble_config.l_level_on_move_max = int(
                event.control.value)

        def rumble_level_r_on_start_slider_callback(event):
            self.core.rumble_config.r_level_on_start = int(event.control.value)

        def rumble_level_r_on_move_max_slider_callback(event):
            self.core.rumble_config.r_level_on_move_max = int(
                event.control.value)

        page.add(
            ft.AppBar(
                title=ft.Text(APP_TITLE),
                bgcolor=ft.colors.SURFACE_VARIANT,
                actions=[
                    ft.PopupMenuButton(
                        items=[
                            ft.PopupMenuItem(
                                text="OSSライセンス",
                                on_click=self._show_oss_license,
                            ),
                        ]
                    ),
                ],
            ),
            ft.ElevatedButton(
                "コントローラー L を接続する",
                on_click=self._connect_l_button_clicked,
            ),
            ft.Text("開始時の振動の強さ"),
            ft.Slider(
                min=0, max=11, divisions=11, label="{value}",
                value=self.core.rumble_config.l_level_on_start,
                on_change=rumble_level_l_on_start_slider_callback,
            ),
            ft.Text("継続中の振動の強さ（最大値）"),
            ft.Slider(
                min=0, max=11, divisions=11, label="{value}",
                value=self.core.rumble_config.l_level_on_move_max,
                on_change=rumble_level_l_on_move_max_slider_callback,
            ),
            ft.Divider(),
            ft.ElevatedButton(
                "コントローラー R を接続する",
                on_click=self._connect_r_button_clicked,
            ),
            ft.Text("開始時の振動の強さ"),
            ft.Slider(
                min=0, max=11, divisions=11, label="{value}",
                value=self.core.rumble_config.r_level_on_start,
                on_change=rumble_level_r_on_start_slider_callback,
            ),
            ft.Text("継続中の振動の強さ（最大値）"),
            ft.Slider(
                min=0, max=11, divisions=11, label="{value}",
                value=self.core.rumble_config.r_level_on_move_max,
                on_change=rumble_level_r_on_move_max_slider_callback,
            ),
        )
        is_outdated, message_from_new_version\
            = VersionChecker.is_newer_version_available(VERSION)
        if is_outdated:
            dialog = ft.AlertDialog(
                title=ft.Text("更新のお知らせ"),
                content=ft.Column(
                    [
                        ft.Text(message_from_new_version),
                        ft.Text(spans=[
                            ft.TextSpan(
                                text="ダウンロードページへ",
                                style=ft.TextStyle(
                                    decoration=ft.TextDecoration.UNDERLINE
                                ),
                                url=DOWNLOAD_LINK,
                            ),
                        ])
                    ],
                    scroll="always",
                ),
            )
            page.dialog = dialog
            dialog.open = True
            page.update()

    def _connect_l_button_clicked(self, event):
        if self.core.connect_controller("L"):
            pass
        else:
            dialog = ft.AlertDialog(
                title=ft.Text("コントローラー L を接続できませんでした")
            )
            event.page.dialog = dialog
            dialog.open = True
            event.page.update()

    def _connect_r_button_clicked(self, event):
        if self.core.connect_controller("R"):
            pass
        else:
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
