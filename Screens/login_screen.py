from kivy.uix.screenmanager import Screen
from kivy.app import App

# class for the login screen
class LoginScreen(Screen):
    # functions that run before entering the screen
    def on_pre_enter(self, *args):
        app = App.get_running_app()
        
        # getting user's name and refreshing the theme to fit their preferences
        user = getattr(app, 'current_user', None)
        username = None
        if isinstance(user, dict):
            username = user.get('username')
            
        app.refresh_theme(username)
    
    # functions that run when entering the screen
    def on_enter(self, *args):
        app = App.get_running_app()
        
        # getting the user's name and refreshing the screen to fit their preferences
        user = getattr(app, 'current_user', None)
        username = None
        if isinstance(user, dict):
            username = user.get('username')
        
        app.refresh_theme(username)
    
    # function to log the user in when pressing the login button
    def do_login(self, username, password):
        app = App.get_running_app()
        
        # attempting to authenticate the user using the auth_service class
        ok, res = app.auth.login(username, password)
        if ok:                  # if the user successfully logs in 
            app.current_user = res      # setting the current_user attribute to the be the logged in user
            
            # getting user's name and refreshing the screen based on the their preferences
            user = getattr(app, 'current_user', None)
            username = None
            if isinstance(user, dict):
                username = user.get('username')         
            
            app.refresh_theme(username)
                
            app.goto("dashboard")           # sending user to the dashboard
            
        else:
            print("Login failed:", res)     # error message shown when log in fails
