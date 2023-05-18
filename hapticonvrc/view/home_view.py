import flet as ft

from ..core import Core


class HomeView(ft.View):
    def __init__(self, page: ft.Page, core: Core):
        self._core = core
        self._core.view = self
        #
        self._app_bar = ft.AppBar(
            title=ft.Text("Test app"),
            bgcolor=ft.colors.SURFACE_VARIANT,
        )
        self._position_text = ft.Text()
        self._connect_controllers_button = ft.ElevatedButton(
            "Connect Controllers",
            on_click=self._connect_controllers_button_clicked,
        )
        self._start_osc_server_button = ft.ElevatedButton(
            "Start OSC-Server",
            on_click=self._start_osc_server_button_clicked,
        )
        self._oss_button = ft.ElevatedButton(
            "OSS License",
            on_click=lambda _: page.go("/osslicense"),
        )
        super().__init__(
            route="/",
            controls=[
                self._app_bar,
                self._connect_controllers_button,
                self._start_osc_server_button,
                self._position_text,
                self._oss_button,
            ],
        )

    def _connect_controllers_button_clicked(self, _):
        self._core.connect_controllers()

    def _start_osc_server_button_clicked(self, _):
        self._start_osc_server_button.disabled = True
        self._core.start_tail_tracker()

    def on_position_updated(self, position):
        self._position_text.value = str(position)
        self.page.update()
