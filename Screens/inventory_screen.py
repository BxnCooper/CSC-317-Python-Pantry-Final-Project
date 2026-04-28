from kivy.uix.screenmanager import Screen


class InventoryScreen(Screen):
    def refresh(self):
        app = self.manager.app
        items = app.backend.get("inventory_service").list_items()
        self.ids.inv_list.clear_widgets()
        for it in items:
            from kivy.uix.label import Label
            self.ids.inv_list.add_widget(Label(text=f"{it['name']}: {it['stock']}"))
