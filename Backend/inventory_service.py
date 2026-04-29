from Backend.database import Database

class InventoryManagement():
    def __init__(self):
        self.inventory = Database()
    
    def list_items(self):
        return self.inventory.list_inventory()

    def list_items_by_name(self):
        return self.inventory.list_inventory_name()
        
    def list_items_by_stock(self):
        return self.inventory.list_inventory_stock()
        
    def list_items_by_allergens(self):
        return self.inventory.list_inventory_allergen()

    def get_id(self, name: str):
        return self.inventory.get_item(name)

    def change_stock(self, name: str, delta: int):
        item_id = self.get_id(name)
        
        return self.inventory.change_stock(item_id, delta)

    def add_item(self, name: str, stock: int, allergens: str):
        return self.inventory.add_item(name, stock, allergens)

    def remove_item(self, name: str):
        id = self.get_id(name)
        
        return self.inventory.remove_item(id)

if __name__ == '__main__':
    test_inv = InventoryManagement()
    
    print(str(test_inv.list_items()))
    # print(str(change_stock(1, -200)))
    # add_item("Frozen Meals", 105)
    # print(remove_item(6))
    print(test_inv.get_id("Mac and Cheese"))