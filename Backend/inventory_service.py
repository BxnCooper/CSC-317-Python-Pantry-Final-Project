from Backend.database import list_inventory, get_item, remove_item as db_remove_item, add_item as db_add_item, change_stock as db_change_stock


def list_items():
    return list_inventory()

def get_id(name: str):
    return get_item(name)

def change_stock(name: str, delta: int):
    item_id = get_id(name)
    
    return db_change_stock(item_id, delta)

def add_item(name: str, stock: int, allergens: str):
    return db_add_item(name, stock, allergens)

def remove_item(name: str):
    id = get_id(name)
    
    return db_remove_item(id)

if __name__ == '__main__':
    print(str(list_items()))
    # print(str(change_stock(1, -200)))
    # add_item("Frozen Meals", 105)
    # print(remove_item(6))
    print(get_item("Mac and Cheese"))