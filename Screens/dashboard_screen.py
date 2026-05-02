from kivy.uix.screenmanager import Screen
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label

class DashboardScreen(Screen):
    def on_pre_enter(self, *args):        
        app = App.get_running_app()
        
        user = getattr(app, 'current_user', None)
        username = None
        if isinstance(user, dict):
            username = user.get('username')
        
        if not username:
            self.ids.welcome_txt.text = 'Welcome back Guest!'
        else:
            self.ids.welcome_txt.text = f'Welcome back {username}!'
        
        app.refresh_theme(username)
        
        # gets the list of items from the database
        items = app.inventory.list_items()
        self.ids.inv_list_dash.clear_widgets()       # clears widgets from the inv_list to prevent duplicates
        
        # creates the labels that are above the items in the inventory to give context
        label_box = b = BoxLayout(size_hint_y=None, height=48)
        label_box.add_widget(Label(text="Item Name", color=app.text_color, font_size=app.fs_xl))
        label_box.add_widget(Label(text="Stock", color=app.text_color, font_size=app.fs_xl, size_hint_x=None, width=80))
        self.ids.inv_list_dash.add_widget(label_box)
        
        # adding each item with 25 or less stock to the inv_list_dash widget
        for it in items:
            if it.get('stock') <= 25:
                b = BoxLayout(size_hint_y=None, height=48)
                b.add_widget(Label(text=it.get('name'), font_size=app.fs_lg, color=app.text_color))
                b.add_widget(Label(text=str(it.get('stock')), font_size=app.fs_lg, color=app.text_color, size_hint_x=None, width=80))
                self.ids.inv_list_dash.add_widget(b)
        
    def on_enter(self, *args):
        app = App.get_running_app()
        
        user = getattr(app, 'current_user', None)
        username = None
        if isinstance(user, dict):
            username = user.get('username')
        
        if not username:
            self.ids.welcome_txt.text = 'Welcome back Guest!'
        else:
            self.ids.welcome_txt.text = f'Welcome back {username}!'
        
        app.refresh_theme(username)
        
        # gets the list of items from the database
        items = app.inventory.list_items_by_stock()
        self.ids.inv_list_dash.clear_widgets()       # clears widgets from the inv_list to prevent duplicates
        
        # creates the labels that are above the items in the inventory to give context
        label_box = b = BoxLayout(size_hint_y=None, height=48)
        label_box.add_widget(Label(text="Item Name", color=app.text_color, font_size=app.fs_xl))
        label_box.add_widget(Label(text="Stock", color=app.text_color, font_size=app.fs_xl, size_hint_x=None, width=80))
        self.ids.inv_list_dash.add_widget(label_box)
        
        # adding each item with 25 or less stock to the inv_list_dash widget
        for it in items:
            if it.get('stock') <= 25:
                b = BoxLayout(size_hint_y=None, height=48)
                b.add_widget(Label(text=it.get('name'), color=app.text_color, font_size=app.fs_lg))
                b.add_widget(Label(text=str(it.get('stock')), color=app.text_color, font_size=app.fs_lg, size_hint_x=None, width=80))
                self.ids.inv_list_dash.add_widget(b)
        
    def logout_user(self):
        app = App.get_running_app()
        app.current_user = None
        user = None
        username = None
        app.goto("login")
        
