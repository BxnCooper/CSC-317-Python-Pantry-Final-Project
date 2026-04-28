from kivy.uix.screenmanager import Screen
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout


class VolunteerPortalScreen(Screen):
    def on_pre_enter(self):
        app = App.get_running_app()
        container = self.ids.get('volunteer_list')
        if not container:
            return
        container.clear_widgets()

        # For now volunteers are simple placeholders; future: wire to a volunteer_service
        volunteers = [
            {"name": "Morning Shift - Mon", "info": "8am-11am"},
            {"name": "Afternoon Shift - Wed", "info": "1pm-4pm"},
        ]

        for v in volunteers:
            b = BoxLayout(size_hint_y=None, height=48)
            b.add_widget(Label(text=v['name'], color=app.text_color))
            b.add_widget(Label(text=v['info'], color=app.text_color, size_hint_x=None, width=120))
            container.add_widget(b)
