from kivy.uix.screenmanager import Screen


class RegisterScreen(Screen):
    def do_register(self, username, password):
        app = self.manager.app
        ok, res = app.backend.get("auth_service").register(username, password)
        if ok:
            app.goto("login")
        else:
            print("Register failed:", res)
