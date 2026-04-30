from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.properties import StringProperty, NumericProperty, ObjectProperty
from kivy.app import App
from kivy.graphics import Color, Rectangle, RoundedRectangle
from kivy.metrics import dp
from kivy.core.window import Window
from kivy.lang import Builder

# small helper to set a background color for widgets
def _set_bg(widget, color):
    with widget.canvas.before:
        Color(*color)
        widget._bg_rect = Rectangle(pos=widget.pos, size=widget.size)
    def _upd(instance, value):
        widget._bg_rect.pos = widget.pos
        widget._bg_rect.size = widget.size
    widget.bind(pos=_upd, size=_upd)

# card widget 
class Card(BoxLayout):
    title = StringProperty("")

    def on_kv_post(self, base_widget):
        app = App.get_running_app()
        if app:
            try:
                self.padding = dp(12)
                self.spacing = dp(8)
                _set_bg(self, app.primary)
            except Exception:
                pass


class CardLabel(Label):
    pass

# card widget for the donor screen
class DonorCard(BoxLayout):
    name = StringProperty("")
    info = StringProperty("")

    def on_kv_post(self, base_widget):
        app = App.get_running_app()
        if app:
            # provide background and text color
            try:
                _set_bg(self, app.surface)
                self.ids.name_label.color = app.text_color
            except Exception:
                pass

# header object that is on every screen
class HeaderBar(BoxLayout):
    title = StringProperty('Pantry')

    def on_kv_post(self, base_widget):
        app = App.get_running_app()
        try:
            self.height = dp(56)
            self.padding = [dp(12), dp(8)]
            _set_bg(self, app.primary)
        except Exception:
            pass

# styled card widget that is on some screens
class StyledCard(BoxLayout):
    title = StringProperty("")

    def on_kv_post(self, base_widget):
        app = App.get_running_app()
        try:
            self.padding = dp(12)
            self.spacing = dp(8)
            _set_bg(self, app.primary)
        except Exception:
            pass

