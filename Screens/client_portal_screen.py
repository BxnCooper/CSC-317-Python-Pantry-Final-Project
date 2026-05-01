from kivy.uix.screenmanager import Screen
from kivy.app import App


# list of common allergens that clients can select from
ALLERGENS = ["Gluten", "Dairy", "Eggs", "Nuts", "Soy", "Shellfish", "Fish", "Sesame"]


class ClientPortalScreen(Screen):

    def on_pre_enter(self):
        # refresh the theme before the screen is shown
        app = App.get_running_app()
        user = getattr(app, 'current_user', None)
        username = user.get('username') if isinstance(user, dict) else None
        app.refresh_theme(username)
        # build the allergen checkboxes every time we enter the screen
        # so that saved allergens are always loaded fresh from the database
        self.build_allergen_checkboxes()

    def on_enter(self, *args):
        # re-apply theme when fully entered (handles edge cases with transitions)
        app = App.get_running_app()
        user = getattr(app, 'current_user', None)
        username = user.get('username') if isinstance(user, dict) else None
        app.refresh_theme(username)

    def build_allergen_checkboxes(self):
        """Dynamically build one checkbox row per allergen.
        If the current user already has saved allergens, pre-check those boxes."""

        container = self.ids.get('allergen_list')
        if not container:
            return
        # clear old widgets so we don't duplicate rows on re-entry
        container.clear_widgets()

        app = App.get_running_app()
        user = getattr(app, 'current_user', None)
        username = user.get('username') if isinstance(user, dict) else None

        # fetch the user's previously saved allergens from the database
        saved = []
        if username:
            raw = app.db.get_user_allergens(username)
            if raw:
                # split the comma-separated string back into a list
                saved = [a.strip() for a in raw.split(',')]

        from kivy.uix.boxlayout import BoxLayout
        from kivy.uix.label import Label
        from kivy.uix.checkbox import CheckBox

        # create one row per allergen with a checkbox and a label
        for allergen in ALLERGENS:
            row = BoxLayout(orientation='horizontal', size_hint_y=None, height='40dp', spacing='8dp')

            cb = CheckBox(
                size_hint_x=None,
                width='40dp',
                active=(allergen in saved),  # pre-check if already saved
                color=app.text_color
            )
            # tag the checkbox with the allergen name so we can read it back later
            cb.allergen_name = allergen

            lbl = Label(
                text=allergen,
                color=app.text_color,
                halign='left',
                valign='middle'
            )
            # make the label wrap text properly inside its box
            lbl.bind(size=lambda inst, val: setattr(inst, 'text_size', val))

            row.add_widget(cb)
            row.add_widget(lbl)
            container.add_widget(row)

    def do_register_client(self, username, password):
        """Handle the Register Client button press.
        Validates input, calls auth service, and redirects to login on success."""

        app = App.get_running_app()

        # make sure neither field is empty before trying to register
        if not username.strip() or not password.strip():
            self.ids.status_label.text = "Username and password required."
            return

        # use the same auth service register flow the rest of the app uses
        ok, res = app.auth.register(username.strip(), password.strip())

        if ok:
            # clear the form and send the user to login
            self.ids.status_label.text = "Account created! Please log in."
            self.ids.reg_username.text = ''
            self.ids.reg_password.text = ''
            app.goto('login')
        else:
            # show the error returned by auth service (e.g. "User exists")
            self.ids.status_label.text = "Registration failed: " + str(res)

    def save_allergens(self):
        """Read which checkboxes are checked and save them to the database
        as a comma-separated string under the logged-in user's record."""

        app = App.get_running_app()
        user = getattr(app, 'current_user', None)
        username = user.get('username') if isinstance(user, dict) else None

        # allergens can only be saved if a user is logged in
        if not username:
            self.ids.allergen_status.text = "You must be logged in to save allergens."
            return

        container = self.ids.get('allergen_list')
        if not container:
            return

        from kivy.uix.checkbox import CheckBox

        # loop through every row in the allergen list and collect checked ones
        selected = []
        for row in container.children:
            for child in row.children:
                # only look at CheckBox widgets, skip Labels
                if isinstance(child, CheckBox) and child.active:
                    selected.append(child.allergen_name)

        # join selected allergens into a comma-separated string for storage
        allergen_str = ', '.join(selected)

        # write to the database
        ok = app.db.update_user_allergens(username, allergen_str)
        if ok:
            self.ids.allergen_status.text = "Allergens saved!"
        else:
            self.ids.allergen_status.text = "Failed to save allergens."