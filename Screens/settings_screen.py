from kivy.uix.screenmanager import Screen
from kivy.app import App
from Backend.database import Database

# class for the settings screen
class SettingsScreen(Screen):
    # functions that run before entering the screen
    def on_pre_enter(self, *args):
        self.db = Database()
        
        # getting the user's name and refreshing screen to fit user preferences
        app = App.get_running_app()
        
        user = getattr(app, 'current_user', None)
        username = None
        if isinstance(user, dict):
            username = user.get('username')
        
        app.refresh_theme(username)
        
    
    # functions that run when entering the screen
    def on_enter(self, *args):
        app = App.get_running_app()
        
        # getting user's name and refreshing to fit user's preferences
        user = getattr(app, 'current_user', None)
        username = None
        if isinstance(user, dict):
            username = user.get('username')
        
        app.refresh_theme(username)
        
        self.ids.status_txt.text = ''
        
    # toggles the dark mode based on if the user presses the light or dark button
    def toggle_dark(self, enabled: bool):
        app = App.get_running_app()
        
        # getting the user's name so that the database can be updated
        # also refreshes screen to show applied changes
        user = getattr(app, 'current_user', None)
        if not user:
            app.goto('login')
            return
        username = user.get('username')
        
        if username:
        
            # updating user preferences in database
            self.db.update_user_theme(username, enabled)
            
            app.refresh_theme(username)
        
        else:
            self.ids.status_txt.text = 'Please sign in to change settings.'
        

    # sets the font size based on which size button the user presses
    def set_font(self, size_name: str):
        app = App.get_running_app()
        
        # getting the user's name so the database can be updates
        # also refreshes the screen to show applied changes
        user = getattr(app, 'current_user', None)
        if not user:
            app.goto('login')
            return
        username = user.get('username')
        
        if username:
            # updating user preferences in database
            self.db.update_user_font(username, size_name)
            
            app.refresh_theme(username)
        
        else:
            self.ids.status_txt.text = 'Please sign in to change settings.'
            
    # function that checks if the user is signed in before sending to confirm screen
    def delete_clicked(self):
        app = App.get_running_app()
        
        # getting the user's name so the database can be updates
        # also refreshes the screen to show applied changes
        user = getattr(app, 'current_user', None)
        if not user:
            app.goto('login')
            return
        username = user.get('username')
        
        if username:
            app.goto('confirm')
        
        else:
            self.ids.status_txt.text = 'Please sign in to change settings.'