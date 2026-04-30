from kivy.uix.screenmanager import Screen
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button


# class for volunteer portal screen
class VolunteerPortalScreen(Screen):
    # functions that run before entering the screen
    def on_pre_enter(self):
        """Load volunteer shifts from the backend and display sign-up state."""
        app = App.get_running_app()
        
        # getting user's name and refreshing screen based on user's preferences
        user = getattr(app, 'current_user', None)
        username = None
        if isinstance(user, dict):
            username = user.get('username')
        
        app.refresh_theme(username)
        
        
        # gets the widget for the volunteer list
        container = self.ids.get('volunteer_list')
        if not container:
            return
        container.clear_widgets()   # clears items from the list

        # fills list with the volunteer slots from the database
        volunteers = []
        try:
            volunteers = app.db.list_volunteers()
        except Exception:
            volunteers = []

        # if there are no volunteers, set special message
        if not volunteers:
            container.add_widget(Label(text='No volunteer opportunities', color=app.text_color, size_hint_y=None, height=40))
            return

        # adding each volunteer slot to the volunteer_list
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

            # gets info about how many people have signed up for each slot
            taken = []
            try:
                taken = app.db.list_shift_signups(v.get('id'))
            except Exception:
                taken = []
            seats = f"{len(taken)}/{v.get('slots',1)}"
            b.add_widget(Label(text=seats, color=app.text_color, font_size=app.fs_sm, size_hint_x=None, width=80))

            # decides if the button should say cancel or sign up based on if the user is already signed up
            if username:
                if username in taken:
                    btn = Button(text='Cancel', font_size=app.fs_md, size_hint_x=None, width=96)
                    btn.bind(on_release=lambda inst, sid=v.get('id'): self.cancel_signup(sid))
                else:
                    btn = Button(text='Sign Up', font_size=app.fs_md, size_hint_x=None, width=96)
                    btn.bind(on_release=lambda inst, sid=v.get('id'): self.sign_up(sid))
            # if the user signs in on the blank account, will not let you sign in
            else:
                btn = Button(text='Login to sign up', font_size=app.fs_md, size_hint_x=None, width=140)
                btn.bind(on_release=lambda *_: app.goto('login'))

            # adding each volunteer slot to the volunteer_list
            b.add_widget(btn)
            container.add_widget(b)

    # function that runs when entering the screen
    # just used to change the screen based on user's preferences
    def on_enter(self, *args):
        app = App.get_running_app()
        
        user = getattr(app, 'current_user', None)
        username = None
        if isinstance(user, dict):
            username = user.get('username')
        
        app.refresh_theme(username)


    # function to sign up for a shift
    def sign_up(self, shift_id: int):
        app = App.get_running_app()
        
        # getting the user's information when attempting to sign up for a slot
        user = getattr(app, 'current_user', None)
        if not user:
            app.goto('login')   # sending user to log in if not logged in
            return
        
        # getting username and adding them to the database as signe dup
        username = user.get('username')
        ok, reason = app.db.sign_up(username, shift_id)
        if not ok:
            print('Failed to sign up:', reason)
        # refresh list
        self.on_pre_enter()

    # function to cancel the signup for the list
    def cancel_signup(self, shift_id: int):
        app = App.get_running_app()
        
        # getting user's information when attempting to cancel
        user = getattr(app, 'current_user', None)
        # if user is not signed in, they cannot hit the cancel button so just return
        if not user:
            return
        
        # gets user's name and cancels their signup in the database
        username = user.get('username')
        ok = app.db.cancel_signup(username, shift_id)
        if not ok:
            print('Failed to cancel signup')
        # refresh list
        self.on_pre_enter()