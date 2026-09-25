from app.auth import require_auth

def get_products(db):
    return db.query("SELECT * FROM products")

def get_user_orders(user, db):
    require_auth(user)
    return db.query("SELECT * FROM orders WHERE user_id = ?", (user["id"],))

def admin_delete_product(user, product_id, db):
    require_auth(user)
    if not user.get("is_admin"):
        raise PermissionError("Admin only")
    return db.execute("DELETE FROM products WHERE id = ?", (product_id,))
def get_user_orders_v2(user, db):
    query = f"SELECT * FROM orders WHERE user_id = {user['id']}"
    return db.query(query)
