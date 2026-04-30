from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.app import App

# class for the inventory screen
class InventoryScreen(Screen):
    current_sort = "id"     # stores the current sorting for the inventory list
    
    # functions that run before entereing the ap
    def on_pre_enter(self):
        app = App.get_running_app()
        
        # getting the user's name and refreshing the theme based on user's preferences
        user = getattr(app, 'current_user', None)
        username = None
        if isinstance(user, dict):
            username = user.get('username')
        
        app.refresh_theme(username)
        
        
        # gets the list of items from the database
        items = app.inventory.list_items()
        self.ids.inv_list.clear_widgets()       # clears widgets from the inv_list to prevent duplicates
        
        # creates the labels that are above the items in the inventory to give context
        label_box = b = BoxLayout(size_hint_y=None, height=48)
        label_box.add_widget(Label(text="Item Name", color=app.text_color))
        label_box.add_widget(Label(text="Allergens", color=app.text_color))
        label_box.add_widget(Label(text="Stock", color=app.text_color, size_hint_x=None, width=80))
        self.ids.inv_list.add_widget(label_box)
        
        # adding each item to the inv_list widget
        for it in items:
            b = BoxLayout(size_hint_y=None, height=48)
            b.add_widget(Label(text=it.get('name'), color=app.text_color))
            b.add_widget(Label(text=it.get('allergens'), color=app.text_color))
            b.add_widget(Label(text=str(it.get('stock')), color=app.text_color, size_hint_x=None, width=80))
            self.ids.inv_list.add_widget(b)
    
    # functions that runs when entering the screen
    # mostly just used to ensure user preferences apply
    def on_enter(self, *args):
        app = App.get_running_app()
        
        user = getattr(app, 'current_user', None)
        username = None
        if isinstance(user, dict):
            username = user.get('username')
        
        app.refresh_theme(username)
    
    # called when updating something about the inventory or when pressing the refresh button
    # essentially rebuilds the list of items in the inventory
    # the list of items is built based on the sorting preference
    def refresh(self):
        app = App.get_running_app()
        items = app.inventory.list_items()
        self.ids.inv_list.clear_widgets()
        
        label_box = b = BoxLayout(size_hint_y=None, height=48)
        label_box.add_widget(Label(text="Item Name", color=app.text_color))
        label_box.add_widget(Label(text="Allergens", color=app.text_color))
        label_box.add_widget(Label(text="Stock", color=app.text_color, size_hint_x=None, width=80))
        self.ids.inv_list.add_widget(label_box)
        
        # creating the list of items in the order of the selected sort
        match self.current_sort:
            case "id":
                items = app.inventory.list_items()
            case "name":
                items = app.inventory.list_items_by_name()
            case "allergens":
                items = app.inventory.list_items_by_allergens()
            case "stock":
                items = app.inventory.list_items_by_stock()
                
        # adding the items to the screen
        for it in items:
            b = BoxLayout(size_hint_y=None, height=48)
            b.add_widget(Label(text=it.get('name'), color=app.text_color))
            b.add_widget(Label(text=it.get('allergens'), color=app.text_color))
            b.add_widget(Label(text=str(it.get('stock')), color=app.text_color, size_hint_x=None, width=80))
            self.ids.inv_list.add_widget(b)
            
    # adds an item to the database from the screen
    def screen_add_item(self):
        app = App.get_running_app()
        
        # tries to add the item to the database based on what the user enters
        try:
            name = self.ids.add_name_input.text
            stock = int(self.ids.add_stock_input.text)
            allergens = self.ids.add_allergens_input.text
            app.inventory.add_item(name, stock, allergens)
            self.refresh()          # refreshing the screen
            return True
            
        except Exception as e:
            print(str(e))
            return False
        
    # deletes an item from the database from the screen
    def screen_remove_item(self):
        app = App.get_running_app()
        
        # tries to remove the item from the database based on user input
        try:
            name = self.ids.remove_name_input.text 
            app.inventory.remove_item(name)
            self.refresh()      # refreshing screen
            return True
            
        except Exception as e:
            print(str(e))
            return False
            
    
    # edits the stock value of an item from the screen
    def screen_edit_item(self):
        app = App.get_running_app()
        
        # tries to update the stock value in the database from user input
        try:
            name = self.ids.edit_name_input.text 
            change_in_stock = self.ids.edit_stock_input.text 
            app.inventory.change_stock(name, change_in_stock)
            self.refresh()      # refreshing screen
            return True
        
        except Exception as e:
            print(str(e))
            return False

    # sets current_sort to id when pressing the id sort button
    def set_sort_id(self):
        self.current_sort = "id"
        self.refresh()

    # sets current_sort to name when pressing the name sort button
    def set_sort_name(self):
        self.current_sort = "name"
        self.refresh()
        
    # sets current_sort to allergens when pressing the allergens sort button    
    def set_sort_allergens(self):
        self.current_sort = "allergens"
        self.refresh()
      
    # sets current_sort to stock when pressing the stock sort button  
    def set_sort_stock(self):
        self.current_sort = "stock"
        self.refresh()