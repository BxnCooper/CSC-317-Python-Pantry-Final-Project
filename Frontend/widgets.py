from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.properties import StringProperty, NumericProperty, ObjectProperty
from kivy.app import App
from kivy.graphics import Color, RoundedRectangle
from kivy.metrics import dp
from kivy.core.window import Window
from kivy.lang import Builder

# small helper to set a background color for widgets
def _set_bg(widget, color):
    with widget.canvas.before:
        Color(*color)
        widget._bg_rect = RoundedRectangle(pos=widget.pos, size=widget.size, radius=[8])
    def _upd(instance, value):
        widget._bg_rect.pos = widget.pos
        widget._bg_rect.size = widget.size
    widget.bind(pos=_upd, size=_upd)


class Card(BoxLayout):
    title = StringProperty("")

    def on_kv_post(self, base_widget):
        app = App.get_running_app()
        if app:
            try:
                self.padding = dp(12)
                self.spacing = dp(8)
                _set_bg(self, app.card)
            except Exception:
                pass


class CardLabel(Label):
    pass


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


class InventoryRow(BoxLayout):
    item_id = NumericProperty(0)
    name = StringProperty("")
    stock = NumericProperty(0)
    change_callback = ObjectProperty(None)

    def increase(self):
        try:
            app = App.get_running_app()
            ok, res = app.backend.get("inventory_service").change_stock(self.item_id, 1)
            if ok:
                self.stock = res.get("stock", self.stock)
                if callable(self.change_callback):
                    self.change_callback()
        except Exception as e:
            print("Inventory increase failed:", e)

    def decrease(self):
        try:
            app = App.get_running_app()
            ok, res = app.backend.get("inventory_service").change_stock(self.item_id, -1)
            if ok:
                self.stock = res.get("stock", self.stock)
                if callable(self.change_callback):
                    self.change_callback()
        except Exception as e:
            print("Inventory decrease failed:", e)


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


class StyledCard(BoxLayout):
    title = StringProperty("")

    def on_kv_post(self, base_widget):
        app = App.get_running_app()
        try:
            self.padding = dp(12)
            self.spacing = dp(8)
            _set_bg(self, app.card)
        except Exception:
            pass

