from kivy.uix.screenmanager import Screen
from kivy.app import App


class SettingsScreen(Screen):
    def toggle_dark(self, enabled: bool):
        app = App.get_running_app()
        app.apply_theme(dark=enabled, font_size_name=app._font_size_name)

    def set_font(self, size_name: str):
        app = App.get_running_app()
        app._font_size_name = size_name
        app.apply_theme(dark=app._dark, font_size_name=size_name)
