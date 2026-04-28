from backend.database import list_inventory, change_stock as db_change_stock


def list_items():
    return list_inventory()


def change_stock(item_id, delta):
    return db_change_stock(item_id, delta)
