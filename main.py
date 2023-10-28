# Do not modify these lines
__winc_id__ = "d7b474e9b3a54d23bca54879a4f1855b"
__human_name__ = "Betsy Webshop"

# Add your code after this line


from models import db, Users, Tags, Products, ProductTags, Transactions
from peewee import fn


def main() -> None:
    populate_test_database()
    search_products('sweater')
    view_user_products(1)
    

# Populating test data
def populate_test_database():
    # Check if the database is already populated
    if Users.select().exists():
        print("Database already populated. Skipping population.")
        return
    else:
        print("Database is empty. Populating with test data.")
        
    alice = Users.create(name="Alice", address="123 Main St", billing_info="VISA 1234")
    bob = Users.create(name="Bob", address="456 High St", billing_info="AMEX 5678")
    
    sweater_tag = Tags.create(name="sweater")
    gift_tag = Tags.create(name="gift")

    sweater = Products.create(name="Cool Sweater", description="Very cool", price=59.99, quantity=20, owner=alice)
    ProductTags.create(product=sweater, tag=sweater_tag)
    ProductTags.create(product=sweater, tag=gift_tag)


# Search products based on term
def search_products(term):
    query = Products.select().where(
        (fn.Lower(Products.name).contains(term.lower())) | 
        (fn.Lower(Products.description).contains(term.lower()))
    )
    for product in query:
        print(product.name)


# View products of a given user
def view_user_products(user):
    query = Products.select().where(Products.owner == user)
    for product in query:
        print(product.name)

# View all products for a given tag
def view_products_by_tag(tag):
    query = Products.select().join(ProductTags).where(ProductTags.tag == tag)
    for product in query:
        print(product.name)

# Add a product to a user
def add_product_to_user(user, name, description, price, quantity):
    Product.create(name=name, description=description, price=price, quantity=quantity, owner=user)

# Remove a product from a user
def remove_product_from_user(user, product):
    products = Products.select().where(Products.owner == user)
    for p in products:
        if p.name == product.name:
            p.delete_instance()

# Update the stock quantity of a product by name
def update_product_quantity(product_name, new_quantity):
    try:
        product = Products.get(Products.name == product_name)
        product.quantity = new_quantity
        product.save()
    except Products.DoesNotExist:
        print(f"Product with name {product_name} does not exist.")

# Handle a purchase between a buyer and a seller
def handle_purchase(buyer, product, quantity):
    if product.quantity >= quantity:
        Transactions.create(buyer=buyer, product=product, quantity=quantity)
        product.quantity -= quantity
        product.save()
        

if __name__ == '__main__':
    main()