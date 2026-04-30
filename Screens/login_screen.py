from kivy.uix.screenmanager import Screen
from kivy.app import App

class LoginScreen(Screen):
    def do_login(self, username, password):
        app = App.get_running_app()
        ok, res = app.auth.login(username, password)
        if ok:
            app.current_user = res
            app.goto("dashboard")
        else:
            print("Login failed:", res)
