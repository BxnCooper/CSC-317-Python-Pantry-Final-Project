from Backend.database import Database

# class for managing the database inventory
# mostly calls directly to the database, but this makes it more logical when needing to access the inventory
class InventoryManagement():
    # initializes the inventory as the database
    def __init__(self):
        self.inventory = Database()
    
    # lists the items in the inventory by id
    def list_items(self):
        return self.inventory.list_inventory()

    # lists the items in the inventory by name
    def list_items_by_name(self):
        return self.inventory.list_inventory_name()
        
    # lists the items in the inventory by stock
    def list_items_by_stock(self):
        return self.inventory.list_inventory_stock()
        
    # lists the items in the inventory by allergen
    def list_items_by_allergens(self):
        return self.inventory.list_inventory_allergen()

    # gets the id of an item, used when changing the stock and deleting an item
    # this is so the user can just enter the name of the item without needing to know the id
    def get_id(self, name: str):
        return self.inventory.get_item(name)

    def get_stock(self, name: str):
        return self.inventory.get_stock(name)

    # changes the stock value of the object by delta (can be +/-)
    def change_stock(self, name: str, delta: int):
        item_id = self.get_id(name)
        
        return self.inventory.change_stock(item_id, delta)

    # adds an item to the inventory table
    def add_item(self, name: str, stock: int, allergens: str):
        return self.inventory.add_item(name, stock, allergens)

    # removes and item from the inventory table
    def remove_item(self, name: str):
        id = self.get_id(name)
        
        return self.inventory.remove_item(id)


# used for testing inventory functions
if __name__ == '__main__':
    test_inv = InventoryManagement()
    
    print(str(test_inv.list_items()))
    # print(str(change_stock(1, -200)))
    # add_item("Frozen Meals", 105)
    # print(remove_item(6))
    print(test_inv.get_id("Mac and Cheese"))