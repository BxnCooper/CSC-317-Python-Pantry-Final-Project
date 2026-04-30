from kivy.uix.screenmanager import Screen
from kivy.app import App
from Backend.database import Database


class SettingsScreen(Screen):
    def on_pre_enter(self, *args):
        self.db = Database()
        
        app = App.get_running_app()
        
        user = getattr(app, 'current_user', None)
        username = None
        if isinstance(user, dict):
            username = user.get('username')
        
        app.refresh_theme(username)
        
    def on_enter(self, *args):
        app = App.get_running_app()
        
        user = getattr(app, 'current_user', None)
        username = None
        if isinstance(user, dict):
            username = user.get('username')
        
        app.refresh_theme(username)
        

    def toggle_dark(self, enabled: bool):
        app = App.get_running_app()
        
        user = getattr(app, 'current_user', None)
        if not user:
            app.goto('login')
            return
        username = user.get('username')
        
        self.db.update_user_theme(username, enabled)
        
        app.refresh_theme(username)
        

    def set_font(self, size_name: str):
        app = App.get_running_app()
        
        user = getattr(app, 'current_user', None)
        if not user:
            app.goto('login')
            return
        username = user.get('username')
        
        self.db.update_user_font(username, size_name)
        
        app.refresh_theme(username)
