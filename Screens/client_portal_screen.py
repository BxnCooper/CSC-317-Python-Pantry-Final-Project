from kivy.uix.screenmanager import Screen
from kivy.app import App


class ClientPortalScreen(Screen):
    def on_pre_enter(self):
        app = App.get_running_app()
        container = self.ids.get('client_actions')
        if not container:
            return
        container.clear_widgets()

        # Show current inventory as available items to request
        items = []
        try:
            inv = app.backend.get('inventory_service')
            if inv:
                items = inv.list_items()
        except Exception:
            items = []

        from kivy.uix.boxlayout import BoxLayout
        from kivy.uix.label import Label

        if not items:
            container.add_widget(Label(text='No items available', color=app.text_color, size_hint_y=None, height=40))
            return

        label_box = b = BoxLayout(size_hint_y=None, height=48)
        label_box.add_widget(Label(text="Item Name", color=app.text_color))
        label_box.add_widget(Label(text="Allergens", color=app.text_color))
        label_box.add_widget(Label(text="Stock", color=app.text_color, size_hint_x=None, width=80))
        container.add_widget(label_box)

        for it in items:
            b = BoxLayout(size_hint_y=None, height=48)
            b.add_widget(Label(text=it.get('name'), color=app.text_color))
            b.add_widget(Label(text=it.get('allergens'), color=app.text_color))
            b.add_widget(Label(text=str(it.get('stock')), color=app.text_color, size_hint_x=None, width=80))
            container.add_widget(b)
