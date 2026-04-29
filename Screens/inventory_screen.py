from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.app import App

class InventoryScreen(Screen):
    current_sort = "id"
    
    def on_pre_enter(self):
        app = App.get_running_app()
        items = app.inventory.list_items()
        self.ids.inv_list.clear_widgets()
        
        label_box = b = BoxLayout(size_hint_y=None, height=48)
        label_box.add_widget(Label(text="Item Name", color=app.text_color))
        label_box.add_widget(Label(text="Allergens", color=app.text_color))
        label_box.add_widget(Label(text="Stock", color=app.text_color, size_hint_x=None, width=80))
        self.ids.inv_list.add_widget(label_box)
        
        for it in items:
            b = BoxLayout(size_hint_y=None, height=48)
            b.add_widget(Label(text=it.get('name'), color=app.text_color))
            b.add_widget(Label(text=it.get('allergens'), color=app.text_color))
            b.add_widget(Label(text=str(it.get('stock')), color=app.text_color, size_hint_x=None, width=80))
            self.ids.inv_list.add_widget(b)
    
    def refresh(self):
        app = App.get_running_app()
        items = app.inventory.list_items()
        self.ids.inv_list.clear_widgets()
        
        label_box = b = BoxLayout(size_hint_y=None, height=48)
        label_box.add_widget(Label(text="Item Name", color=app.text_color))
        label_box.add_widget(Label(text="Allergens", color=app.text_color))
        label_box.add_widget(Label(text="Stock", color=app.text_color, size_hint_x=None, width=80))
        self.ids.inv_list.add_widget(label_box)
        
        match self.current_sort:
            case "id":
                items = app.inventory.list_items()
            case "name":
                items = app.inventory.list_items_by_name()
            case "allergens":
                items = app.inventory.list_items_by_allergens()
            case "stock":
                items = app.inventory.list_items_by_stock()
                
        for it in items:
            b = BoxLayout(size_hint_y=None, height=48)
            b.add_widget(Label(text=it.get('name'), color=app.text_color))
            b.add_widget(Label(text=it.get('allergens'), color=app.text_color))
            b.add_widget(Label(text=str(it.get('stock')), color=app.text_color, size_hint_x=None, width=80))
            self.ids.inv_list.add_widget(b)
            
    def screen_add_item(self):
        app = App.get_running_app()
        
        try:
            name = self.ids.add_name_input.text
            stock = int(self.ids.add_stock_input.text)
            allergens = self.ids.add_allergens_input.text
            app.inventory.add_item(name, stock, allergens)
            self.refresh()
            return True
            
        except Exception as e:
            print(str(e))
            return False
        
    def screen_remove_item(self):
        app = App.get_running_app()
        
        try:
            name = self.ids.remove_name_input.text 
            app.inventory.remove_item(name)
            self.refresh()
            return True
            
        except Exception as e:
            print(str(e))
            return False
            
        
    def screen_edit_item(self):
        app = App.get_running_app()
        
        try:
            name = self.ids.edit_name_input.text 
            change_in_stock = self.ids.edit_stock_input.text 
            app.inventory.change_stock(name, change_in_stock)
            self.refresh()
            return True
        
        except Exception as e:
            print(str(e))
            return False

    def set_sort_id(self):
        self.current_sort = "id"
        self.refresh()

    def set_sort_name(self):
        self.current_sort = "name"
        self.refresh()
        
    def set_sort_allergens(self):
        self.current_sort = "allergens"
        self.refresh()
        
    def set_sort_stock(self):
        self.current_sort = "stock"
        self.refresh()