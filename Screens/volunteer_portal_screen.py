from kivy.uix.screenmanager import Screen
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button


class VolunteerPortalScreen(Screen):
    def on_pre_enter(self):
        """Load volunteer shifts from the backend and display sign-up state."""
        app = App.get_running_app()
        
        user = getattr(app, 'current_user', None)
        username = None
        if isinstance(user, dict):
            username = user.get('username')
        
        app.refresh_theme(username)
        
        container = self.ids.get('volunteer_list')
        if not container:
            return
        container.clear_widgets()

        volunteers = []
        try:
            volunteers = app.db.list_volunteers()
        except Exception:
            volunteers = []

        if not volunteers:
            container.add_widget(Label(text='No volunteer opportunities', color=app.text_color, size_hint_y=None, height=40))
            return

        for v in volunteers:
            b = BoxLayout(size_hint_y=None, height=64, spacing=8)

            # Left column: title (day/shift) on top, time/date underneath
            left = BoxLayout(orientation='vertical')
            title = Label(text=v.get('name', ''), color=app.text_color, font_size=app.fs_lg, halign='left', valign='middle')
            # smaller font for the time/date line
            info_lbl = Label(text=v.get('info', ''), color=app.text_color, font_size=app.fs_sm, halign='left', valign='middle')
            # ensure labels use full width in the vertical box
            title.size_hint_y = None
            title.height = 28
            info_lbl.size_hint_y = None
            info_lbl.height = 20
            left.add_widget(title)
            left.add_widget(info_lbl)
            b.add_widget(left)

            # seat info
            taken = []
            try:
                taken = app.db.list_shift_signups(v.get('id'))
            except Exception:
                taken = []
            seats = f"{len(taken)}/{v.get('slots',1)}"
            b.add_widget(Label(text=seats, color=app.text_color, font_size=app.fs_sm, size_hint_x=None, width=80))

            # action button: sign up or cancel
            if username:
                if username in taken:
                    btn = Button(text='Cancel', font_size=app.fs_md, size_hint_x=None, width=96)
                    btn.bind(on_release=lambda inst, sid=v.get('id'): self.cancel_signup(sid))
                else:
                    btn = Button(text='Sign Up', font_size=app.fs_md, size_hint_x=None, width=96)
                    btn.bind(on_release=lambda inst, sid=v.get('id'): self.sign_up(sid))
            else:
                btn = Button(text='Login to sign up', font_size=app.fs_md, size_hint_x=None, width=140)
                btn.bind(on_release=lambda *_: app.goto('login'))

            b.add_widget(btn)
            container.add_widget(b)

    def on_enter(self, *args):
        app = App.get_running_app()
        
        user = getattr(app, 'current_user', None)
        username = None
        if isinstance(user, dict):
            username = user.get('username')
        
        app.refresh_theme(username)

    def sign_up(self, shift_id: int):
        app = App.get_running_app()
        user = getattr(app, 'current_user', None)
        if not user:
            app.goto('login')
            return
        username = user.get('username')
        ok, reason = app.db.sign_up(username, shift_id)
        if not ok:
            print('Failed to sign up:', reason)
        # refresh list
        self.on_pre_enter()

    def cancel_signup(self, shift_id: int):
        app = App.get_running_app()
        user = getattr(app, 'current_user', None)
        if not user:
            return
        username = user.get('username')
        ok = app.db.cancel_signup(username, shift_id)
        if not ok:
            print('Failed to cancel signup')
        self.on_pre_enter()