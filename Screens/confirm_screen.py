from kivy.uix.screenmanager import Screen
from kivy.app import App

# class for the confirm screen
class ConfirmScreen(Screen):
    # functions that run before entering the screen
    def on_pre_enter(self, *args):
        # getting the username of the logged in user and refreshing the theme based on preference
        app = App.get_running_app()
        
        user = getattr(app, 'current_user', None)
        username = None
        if isinstance(user, dict):
            username = user.get('username')
        
        app.refresh_theme(username)
    
    # functions that run every time the screen is entered
    def on_enter(self, *args):
        # getting the username of the logged in user and refreshing the theme based on preference
        app = App.get_running_app()
        
        user = getattr(app, 'current_user', None)
        username = None
        if isinstance(user, dict):
            username = user.get('username')
        
        app.refresh_theme(username)
    
    # function that resets all of the user's data in the database and logs them out
    def reset_data(self):
        # getting the user's name
        app = App.get_running_app()
        
        user = getattr(app, 'current_user', None)
        username = None
        if isinstance(user, dict):
            username = user.get('username')
            
        # updating the user's preferences in the database to be the default values
        app.db.update_user_theme(username, False)
        app.db.update_user_font(username, "Medium")
        app.db.update_user_allergens(username, "None")
        
        # logging the user out and sending them to the login screen
        app.current_user = None
        user = None
        username = None
        app.goto("login")