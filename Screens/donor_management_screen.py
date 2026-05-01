from kivy.uix.screenmanager import Screen
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.graphics import Color, RoundedRectangle
from kivy.metrics import dp


class DonorCard(BoxLayout):
    """A card widget displaying one donor's details."""

    def __init__(self, donor: dict, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.padding = dp(12)
        self.spacing = dp(6)
        self.size_hint_y = None
        self.height = dp(160)

        app = App.get_running_app()
        surface = getattr(app, "surface", (0.85, 0.80, 0.78, 1))
        primary = getattr(app, "primary", (0.72, 0.65, 0.62, 1))
        text_color = getattr(app, "text_color", (0, 0, 0, 1))

        # rounded card background
        with self.canvas.before:
            Color(*surface)
            self._bg = RoundedRectangle(pos=self.pos, size=self.size, radius=[12])
        self.bind(pos=self._update_bg, size=self._update_bg)

        # donor name label (pill style)
        name_box = BoxLayout(size_hint_y=None, height=dp(36))
        name_lbl = Label(
            text=donor.get("name", "Unnamed"),
            color=text_color,
            bold=True,
            size_hint=(None, None),
            size=(dp(130), dp(30)),
            halign="center",
            valign="middle",
        )
        with name_lbl.canvas.before:
            Color(*primary)
            self._pill = RoundedRectangle(pos=name_lbl.pos, size=name_lbl.size, radius=[14])

        def _upd_pill(*_):
            self._pill.pos = name_lbl.pos
            self._pill.size = name_lbl.size
        name_lbl.bind(pos=_upd_pill, size=_upd_pill)

        name_box.add_widget(name_lbl)
        self.add_widget(name_box)

        # four bullet details
        fields = [
            f"• Item: {donor.get('item', '')}",
            f"• Quantity: {donor.get('quantity', '')}",
            f"• Date: {donor.get('date', '')}",
            f"• Status: {donor.get('status', '')}",
        ]
        for field in fields:
            lbl = Label(
                text=field,
                color=text_color,
                halign="left",
                valign="middle",
                size_hint_y=None,
                height=dp(22),
            )
            lbl.bind(size=lambda inst, val: setattr(inst, "text_size", val))
            self.add_widget(lbl)

    def _update_bg(self, *_):
        self._bg.pos = self.pos
        self._bg.size = self.size


class DonorManagementScreen(Screen):

    def _get_username(self):
        app = App.get_running_app()
        user = getattr(app, "current_user", None)
        if isinstance(user, dict):
            return user.get("username")
        return None

    def on_pre_enter(self, *args):
        app = App.get_running_app()
        app.refresh_theme(self._get_username())

    def on_enter(self, *args):
        app = App.get_running_app()
        app.refresh_theme(self._get_username())
        self.load_donors()

    def load_donors(self):
        app = App.get_running_app()
        container = self.ids.get("donor_list")
        if not container:
            return
        container.clear_widgets()

        donors = []
        try:
            donors = app.db.list_donors()
        except Exception as e:
            print(f"Error loading donors: {e}")

        if not donors:
            lbl = Label(
                text="No donors yet. Schedule a pickup above!",
                color=app.text_color,
                size_hint_y=None,
                height=dp(40),
            )
            container.add_widget(lbl)
            return

        for d in donors:
            card = DonorCard(donor=d)
            container.add_widget(card)

    def add_donor(self):
        app = App.get_running_app()

        name = self.ids.name_input.text.strip() if self.ids.get("name_input") else ""
        item = self.ids.item_input.text.strip() if self.ids.get("item_input") else ""
        quantity = self.ids.quantity_input.text.strip() if self.ids.get("quantity_input") else ""
        date = self.ids.date_input.text.strip() if self.ids.get("date_input") else ""
        status = self.ids.status_input.text.strip() if self.ids.get("status_input") else ""
        location = self.ids.location_input.text.strip() if self.ids.get("location_input") else ""

        if not name:
            print("Donor name is required.")
            return

        try:
            ok = app.db.add_donor(name, item, quantity, date, status, location)
            if ok:
                confirm = app.root.get_screen("donor_management_confirm")
                confirm.donor_name = name
                for field_id in ["name_input", "item_input", "quantity_input",
                                  "date_input", "status_input", "location_input"]:
                    inp = self.ids.get(field_id)
                    if inp:
                        inp.text = ""
                app.goto("donor_management_confirm")
            else:
                print("Error saving donor.")
        except Exception as e:
            print(f"Error adding donor: {e}")


class DonorManagementConfirmScreen(Screen):
    donor_name = ""

    def on_pre_enter(self, *args):
        app = App.get_running_app()
        app.refresh_theme(None)
        lbl = self.ids.get("thank_you_label")
        if lbl:
            lbl.text = f"Thank you for your donation\n{self.donor_name}!"

    def go_back(self):
        App.get_running_app().goto("donor_management")
