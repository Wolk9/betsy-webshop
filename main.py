# Do not modify these lines
__winc_id__ = "d7b474e9b3a54d23bca54879a4f1855b"
__human_name__ = "Betsy Webshop"

# Add your code after this line


from models import db, User, Tag, Product, ProductTag, Transaction
from peewee import fn

# Populating test data
def populate_test_database():
    # Check if the database is already populated
    try:
        user = User.select().get()
        print("Database already populated. Skipping population.")
        return
    except User.DoesNotExist:
        print("Database is empty. Populating with test data.")
        
    alice = User.create(name="Alice", address="123 Main St", billing_info="VISA 1234")
    bob = User.create(name="Bob", address="456 High St", billing_info="AMEX 5678")
    
    sweater_tag = Tag.create(name="sweater")
    gift_tag = Tag.create(name="gift")

    sweater = Product.create(name="Cool Sweater", description="Very cool", price=59.99, quantity=20, owner=alice)
    ProductTag.create(product=sweater, tag=sweater_tag)
    ProductTag.create(product=sweater, tag=gift_tag)


# Search products based on term
def search_products(term):
    query = Product.select().where(
        (fn.Lower(Product.name).contains(term.lower())) | 
        (fn.Lower(Product.description).contains(term.lower()))
    )
    return query

# View products of a given user
def view_user_products(user):
    return Product.select().where(Product.owner == user)

# View all products for a given tag
def view_products_by_tag(tag):
    return Product.select().join(ProductTag).where(ProductTag.tag == tag)

# Add a product to a user
def add_product_to_user(user, name, description, price, quantity):
    return Product.create(name=name, description=description, price=price, quantity=quantity, owner=user)

# Remove a product from a user
def remove_product_from_user(user, product):
    product.delete_instance()

# Update the stock quantity of a product
def update_product_quantity(product, new_quantity):
    product.quantity = new_quantity
    product.save()

# Handle a purchase between a buyer and a seller
def handle_purchase(buyer, product, quantity):
    if product.quantity >= quantity:
        Transaction.create(buyer=buyer, product=product, quantity=quantity)
        product.quantity -= quantity
        product.save()

# Populate the test database
populate_test_database()

# Example queries
for product in search_products('sweater'):
    print(product.name)

for product in view_user_products(User.get(User.name == "Bob")):
    print(product.name)

