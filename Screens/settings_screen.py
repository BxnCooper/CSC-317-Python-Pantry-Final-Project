from kivy.uix.screenmanager import Screen


class SettingsScreen(Screen):
    def toggle_dark(self, enabled: bool):
        app = self.manager.app
        app.apply_theme(dark=enabled, font_size_name=app._font_size_name)

    def set_font(self, size_name: str):
        app = self.manager.app
        app._font_size_name = size_name
        app.apply_theme(dark=app._dark, font_size_name=size_name)
