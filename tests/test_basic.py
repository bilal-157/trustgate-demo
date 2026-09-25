from app.models import Product

def test_product_creation():
    p = Product(id=1, name="Book", price=9.99)
    assert p.name == "Book"
    assert p.price == 9.99