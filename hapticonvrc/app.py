import flet as ft

from .view.home_view import HomeView
from .view.osslicense_view import OSSLicenseView
from .core import Core


def main(page: ft.Page):
    page.title = "サンプル"
    core = Core()

    def route_change(route):
        page.views.clear()
        page.views.append(HomeView(page, core))
        if page.route == "/osslicense":
            page.views.append(OSSLicenseView(page))
        page.update()

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)


def start():
    ft.app(target=main)
