from kivy.uix.screenmanager import Screen


class LoginScreen(Screen):
    def do_login(self, username, password):
        app = self.manager.app
        ok, res = app.backend.get("auth_service").login(username, password)
        if ok:
            # store current user info on app for other screens
            app.current_user = res
            app.goto("dashboard")
        else:
            print("Login failed:", res)
