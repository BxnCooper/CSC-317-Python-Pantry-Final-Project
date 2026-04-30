from kivy.uix.screenmanager import Screen
from kivy.app import App

class LoginScreen(Screen):
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
    
    def do_login(self, username, password):
        app = App.get_running_app()
        
        ok, res = app.auth.login(username, password)
        if ok:
            app.current_user = res
            
            user = getattr(app, 'current_user', None)
            username = None
            if isinstance(user, dict):
                username = user.get('username')
            
            app.refresh_theme(username)
                
            app.goto("dashboard")
            
        else:
            print("Login failed:", res)
