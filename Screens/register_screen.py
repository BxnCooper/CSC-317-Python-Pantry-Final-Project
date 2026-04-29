from kivy.uix.screenmanager import Screen
from kivy.app import App

class RegisterScreen(Screen):
    def do_register(self, username, password):
        app = App.get_running_app()
        ok, res = app.auth.register(username, password)
        if ok:
            app.goto("login")
        else:
            print("Register failed:", res)
