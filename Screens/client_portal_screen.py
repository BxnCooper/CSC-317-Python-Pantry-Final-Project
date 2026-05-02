from kivy.uix.screenmanager import Screen
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label


# list of common allergens that clients can select from
ALLERGENS = ["Gluten", "Dairy", "Eggs", "Nuts", "Soy", "Shellfish", "Fish", "Sesame"]


class ClientPortalScreen(Screen):

    def on_pre_enter(self):
        # refresh the theme before the screen is shown
        app = App.get_running_app()
        user = getattr(app, 'current_user', None)
        username = user.get('username') if isinstance(user, dict) else None
        app.refresh_theme(username)
        
        # gets the list of items from the database
        items = app.inventory.list_items()
        self.ids.inv_list_client.clear_widgets()       # clears widgets from the inv_list to prevent duplicates
        
        # creates the labels that are above the items in the inventory to give context
        label_box = BoxLayout(size_hint_y=None, height=48)
        label_box.add_widget(Label(text="Item Name", font_size=app.fs_xl, color=app.text_color))
        label_box.add_widget(Label(text="Allergens", font_size=app.fs_xl, color=app.text_color))
        label_box.add_widget(Label(text="Stock", font_size=app.fs_xl, color=app.text_color, size_hint_x=None, width=80))
        self.ids.inv_list_client.add_widget(label_box)
        
        # fetch the user's previously saved allergens from the database
        saved = []
        allergen_split = []
        if username:
            raw = app.db.get_user_allergens(username)
            if raw:
                # split the comma-separated string back into a list
                saved = [a.strip() for a in raw.split(',')]
        
        # adding each item to the inv_list widget if user is not allergic
        for it in items:
            allergen_split = [a.strip() for a in it.get('allergens').split(' and ')]
            for allergen in allergen_split:
                if allergen not in saved:
                    b = BoxLayout(size_hint_y=None, height=48)
                    b.add_widget(Label(text=it.get('name'), font_size=app.fs_lg, color=app.text_color))
                    b.add_widget(Label(text=it.get('allergens'), font_size=app.fs_lg, color=app.text_color))
                    b.add_widget(Label(text=str(it.get('stock')), font_size=app.fs_lg, color=app.text_color, size_hint_x=None, width=80))
                    self.ids.inv_list_client.add_widget(b)
                    break
                break
        
        # build the allergen checkboxes every time we enter the screen
        # so that saved allergens are always loaded fresh from the database
        self.build_allergen_checkboxes()
        

    def on_enter(self, *args):
        # re-apply theme when fully entered (handles edge cases with transitions)
        app = App.get_running_app()
        user = getattr(app, 'current_user', None)
        username = user.get('username') if isinstance(user, dict) else None
        app.refresh_theme(username)
        
        self.ids.allergen_status.text = ''
        
        # gets the list of items from the database
        items = app.inventory.list_items()
        self.ids.inv_list_client.clear_widgets()       # clears widgets from the inv_list to prevent duplicates
        
        # creates the labels that are above the items in the inventory to give context
        label_box = BoxLayout(size_hint_y=None, height=48)
        label_box.add_widget(Label(text="Item Name", font_size=app.fs_xl, color=app.text_color))
        label_box.add_widget(Label(text="Allergens", font_size=app.fs_xl, color=app.text_color))
        label_box.add_widget(Label(text="Stock", font_size=app.fs_xl, color=app.text_color, size_hint_x=None, width=80))
        self.ids.inv_list_client.add_widget(label_box)
        
        # fetch the user's previously saved allergens from the database
        saved = []
        allergen_split = []
        if username:
            raw = app.db.get_user_allergens(username)
            if raw:
                # split the comma-separated string back into a list
                saved = [a.strip() for a in raw.split(',')]
        
        # adding each item to the inv_list widget is user is not allergic
        for it in items:
            allergen_split = [a.strip() for a in it.get('allergens').split(' and ')]
            for allergen in allergen_split:
                if allergen not in saved:
                    b = BoxLayout(size_hint_y=None, height=48)
                    b.add_widget(Label(text=it.get('name'), font_size=app.fs_lg, color=app.text_color))
                    b.add_widget(Label(text=it.get('allergens'), font_size=app.fs_lg, color=app.text_color))
                    b.add_widget(Label(text=str(it.get('stock')), font_size=app.fs_lg, color=app.text_color, size_hint_x=None, width=80))
                    self.ids.inv_list_client.add_widget(b)
                    break
                break

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
                color=app.text_color,    
            )
            
            # tag the checkbox with the allergen name so we can read it back later
            cb.allergen_name = allergen

            lbl = Label(
                text=allergen,
                color=app.text_color,
                font_size=app.fs_xl,
                halign='left',
                valign='middle'
            )
            # make the label wrap text properly inside its box
            lbl.bind(size=lambda inst, val: setattr(inst, 'text_size', val))

            row.add_widget(cb)
            row.add_widget(lbl)
            container.add_widget(row)

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
            self.on_enter()
        else:
            self.ids.allergen_status.text = "Failed to save allergens."
            
    # function for ordering from the pantry
    def order(self):
        app = App.get_running_app()
        user = getattr(app, 'current_user', None)
        username = user.get('username') if isinstance(user, dict) else None
        
        # if not logged in give error message
        if not username:
            self.ids.inv_stat_txt.text = "You must be logged in order."
            return
    
        item_name = self.ids.order_name.text
        order_amount = self.ids.order_amount.text
        
        # turning entered order amount into an int
        try:
            order_amount = int(order_amount)
        except ValueError as te:
            self.ids.inv_stat_txt.text = 'The order amount is a string. Enter only integers.'
            return
        
        # checking if the item exists
        if isinstance(app.inventory.get_stock(item_name), str):
            self.ids.inv_stat_txt.text = 'That item does not exist. Try entering a different item name.'
            return
        # checking if order amount is less than 1
        elif order_amount < 1:
            self.ids.inv_stat_txt.text = 'You cannot order an amount less than 1.'
            return
        # checking if the ordered amount is more than there is in stock
        elif order_amount > app.inventory.get_stock(item_name):
            self.ids.inv_stat_txt.text = 'You are ordering more of that item than we have. Please enter a lower amount.'
            return
        # ordering the item and reducing its stock in the database
        else:
            app.inventory.change_stock(item_name, (-1 * order_amount))
            self.ids.inv_stat_txt.text = f'{str(order_amount)} {item_name} have been ordered. Thank you!'
            self.ids.order_name.text = ''
            self.ids.order_amount.text = ''
        
        # refreshing screen
        self.on_enter()

    def back(self):
        app = App.get_running_app()
        
        self.ids.inv_stat_txt.text = ''
        app.goto('dashboard')