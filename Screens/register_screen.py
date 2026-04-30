from kivy.uix.screenmanager import Screen
from kivy.app import App

class RegisterScreen(Screen):
    # functions that run when entering the screen
    # does not need a pre_enter for updating user preferences because the user is not logged in
    def on_enter(self, *args):
        app = App.get_running_app()
        
        user = getattr(app, 'current_user', None)
        username = None
        if isinstance(user, dict):
            username = user.get('username')
        
        app.refresh_theme(username)
    
    # register function that is called when pressing the register button
    def do_register(self, username, password):
        app = App.get_running_app()
        
        # attempting to register the user to the database and returning the error message if something goes wrong   
        ok, res = app.auth.register(username, password)
        if ok:
            app.goto("login")
        else:
            print("Register failed:", res)
