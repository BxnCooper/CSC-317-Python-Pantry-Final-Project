from kivy.uix.screenmanager import Screen
from kivy.app import App

class ConfirmScreen(Screen):
    def on_pre_enter(self, *args):
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
        
    def reset_data(self):
        app = App.get_running_app()
        
        user = getattr(app, 'current_user', None)
        username = None
        if isinstance(user, dict):
            username = user.get('username')
            
        app.db.update_user_theme(username, False)
        app.db.update_user_font(username, "Medium")
        app.db.update_user_allergens(username, "None")
        
        app.current_user = None
        user = None
        username = None
        app.goto("login")