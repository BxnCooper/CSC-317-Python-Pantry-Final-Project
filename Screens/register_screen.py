from kivy.uix.screenmanager import Screen
from kivy.app import App

class RegisterScreen(Screen):
    def on_enter(self, *args):
        app = App.get_running_app()
        
        user = getattr(app, 'current_user', None)
        username = None
        if isinstance(user, dict):
            username = user.get('username')
        
        app.refresh_theme(username)
    
    def do_register(self, username, password):
        app = App.get_running_app()
        
        user = getattr(app, 'current_user', None)
        username = None
        if isinstance(user, dict):
            username = user.get('username')
        
        app.refresh_theme(username)
        
        
        ok, res = app.auth.register(username, password)
        if ok:
            app.goto("login")
        else:
            print("Register failed:", res)
