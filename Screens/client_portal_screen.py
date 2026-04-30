from kivy.uix.screenmanager import Screen
from kivy.app import App


class ClientPortalScreen(Screen):
    def on_pre_enter(self):
        app = App.get_running_app()
        
        user = getattr(app, 'current_user', None)
        username = None
        if isinstance(user, dict):
            username = user.get('username')
        
        app.refresh_theme(username)
        
        
        container = self.ids.get('client_actions')
        if not container:
            return
        container.clear_widgets()

        # Show current inventory as available items to request
        items = []
        try:
            inv = app.inventory
            if inv:
                items = inv.list_items()
        except Exception:
            items = []

        from kivy.uix.boxlayout import BoxLayout
        from kivy.uix.label import Label

        if not items:
            container.add_widget(Label(text='No items available', color=app.text_color, size_hint_y=None, height=40))
            return

        for it in items:
            b = BoxLayout(size_hint_y=None, height=48)
            b.add_widget(Label(text=it.get('name'), color=app.text_color))
            b.add_widget(Label(text=str(it.get('stock')), color=app.text_color, size_hint_x=None, width=80))
            container.add_widget(b)

    def on_enter(self, *args):
        app = App.get_running_app()
        
        user = getattr(app, 'current_user', None)
        username = None
        if isinstance(user, dict):
            username = user.get('username')
        
        app.refresh_theme(username)