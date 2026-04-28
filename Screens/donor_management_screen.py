from kivy.uix.screenmanager import Screen
from kivy.app import App
from kivy.uix.label import Label


class DonorManagementScreen(Screen):
    def on_pre_enter(self):
        """Populate the donor_list GridLayout from the backend database.

        If no donors exist, show a friendly message.
        """
        app = App.get_running_app()
        container = self.ids.get('donor_list')
        if not container:
            return
        # clear existing
        container.clear_widgets()

        donors = []
        try:
            db = app.backend.get('database')
            if db:
                donors = db.read_all().get('donors', [])
        except Exception:
            donors = []

        if not donors:
            container.add_widget(Label(text='No donors yet', color=app.text_color, size_hint_y=None, height=40))
            return

        # lazy import of DonorCard widget registered by Frontend/widgets.py
        try:
            from widgets import DonorCard
        except Exception:
            DonorCard = None

        for d in donors:
            if DonorCard:
                card = DonorCard(name=d.get('name', 'Unnamed'), info=d.get('info', ''))
                card.size_hint_y = None
                card.height = 80
                container.add_widget(card)
            else:
                container.add_widget(Label(text=f"{d.get('name')}: {d.get('info')}", color=app.text_color, size_hint_y=None, height=40))
