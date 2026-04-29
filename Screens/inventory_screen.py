from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout

class InventoryScreen(Screen):
    def on_pre_enter(self):
        app = self.manager.app
        items = app.backend.get("inventory_service").list_items()
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
        app = self.manager.app
        items = app.backend.get("inventory_service").list_items()
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
            
    def screen_add_item(self):
        app = self.manager.app
        
        try:
            name = self.ids.add_name_input.text
            stock = int(self.ids.add_stock_input.text)
            allergens = self.ids.add_allergens_input.text
            app.backend.get("inventory_service").add_item(name, stock, allergens)
            self.refresh()
            return True
            
        except Exception as e:
            print(str(e))
            return False
        
    def screen_remove_item(self):
        app = self.manager.app
        
        try:
            name = self.ids.remove_name_input.text 
            app.backend.get('inventory_service').remove_item(name)
            self.refresh()
            return True
            
        except Exception as e:
            print(str(e))
            return False
            
        
    def screen_edit_item(self):
        app = self.manager.app
        
        try:
            name = self.ids.edit_name_input.text 
            change_in_stock = self.ids.edit_stock_input.text 
            app.backend.get("inventory_service").change_stock(name, change_in_stock)
            self.refresh()
            return True
        
        except Exception as e:
            print(str(e))
            return False
