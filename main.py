# Do not modify these lines
__winc_id__ = "d7b474e9b3a54d23bca54879a4f1855b"
__human_name__ = "Betsy Webshop"

# Add your code after this line


from models import db, Users, Tags, Products, ProductTags, Transactions, init_database
from peewee import fn
from fuzzywuzzy import fuzz


def main() -> None:
    init_database()
    populate_test_database()

    # here you can call the functions you want to test. 
    # I gave some examples below

    # search_products('sweater')
    handle_purchase("Alice", "Cool Sweater", 1)
    handle_purchase("Bob", "Cool Sweater", 1)
    handle_purchase("Bob", "Bottle", 7)
    handle_purchase("Martin", "Cool Sticker", 4)
    # view_user_products('Martin')
    # view_products_by_tag('gift')
    # view_user_products('Bob')
    # remove_product_from_user('Martin', 'Cool Sticker')
    update_product_quantity('Cool Sweater', 10)
    

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
        martin  = Users.create(name="Martin", address="789 Low St", billing_info="MASTERCARD 9012")
        charlie = Users.create(name="Charlie", address="012 Left St", billing_info="VISA 3456")
        fleur = Users.create(name="Fleur", address="789 Right St", billing_info="AMEX 7890")
        
        clothes_tag = Tags.create(name="clothes")
        gift_tag = Tags.create(name="gift")
        disposable_tag = Tags.create(name="disposable")

        sweater = Products.create(name="Cool Sweater", description="Very cool", price=59.99, quantity=20)
        bottle = Products.create(name="Bottle", description="Very cool", price=19.99, quantity=10)
        sticker = Products.create(name="Cool Sticker", description="Very cool", price=9.99, quantity=100) 
        powerbank = Products.create(name="Cool Powerbank", description="Very cool", price=29.99, quantity=50) 
        doormat = Products.create(name="Cool Doormat", description="Very cool", price=39.99, quantity=30)
        
        ProductTags.create(product=sweater, tag=clothes_tag)
        ProductTags.create(product=bottle, tag=gift_tag)
        ProductTags.create(product=doormat, tag=gift_tag)
        ProductTags.create(product=sticker, tag=disposable_tag)
        ProductTags.create(product=powerbank, tag=gift_tag)

        return



# Search products based on term
def search_products(term):
    # Print a message indicating that we're searching for products with the given term
    print(f"Searching for products with term {term}")
    
    # Select all products from the database
    query = Products.select()
    
    # Create an empty list to store the products that match the search term
    matches = []
    
    # Loop through each product in the query
    for product in query:
        # Calculate the fuzzy match ratio between the product name and the search term
        name_ratio = fuzz.ratio(product.name.lower(), term.lower())
        
        # Calculate the fuzzy match ratio between the product description and the search term
        desc_ratio = fuzz.ratio(product.description.lower(), term.lower())
        
        # If either the name or description has a match ratio of 70 or higher, add the product to the matches list
        if name_ratio >= 70 or desc_ratio >= 70:
            matches.append(product)
    
    # If there are any matches, print the names of the matching products
    if matches:
        for product in matches:
            print(product.name)
    # If there are no matches, print a message indicating that no products were found
    else:
        print("No products found.")


# View products of a given user
def view_user_products(user_name):
    # Print a message indicating that we're viewing the products of the given user
    print(f"Viewing products of user {user_name}")
    
    try:
        # Get the user object from the database based on the given user name
        user = Users.get(Users.name == user_name)
        
        # Query the products table to get all products that the user has purchased
        queryOfProducts = Products.select().join(Transactions).where(Transactions.buyer == user)
        
        # Loop through each product in the query results
        for product in queryOfProducts:
            # Get the transaction object that represents the purchase of the product by the user
            transaction = Transactions.get(Transactions.product == product, Transactions.buyer == user)
            
            # Determine whether to use singular or plural form of the product name based on the quantity purchased
            if transaction.quantity > 1:
                plural = "s"
            else:
                plural = ""
            
            # Print a message indicating how many of the product the user has purchased
            print(f"{user_name} has {transaction.quantity} {product.name}{plural}.")
    
    except Users.DoesNotExist:
        # If the user does not exist, print a message indicating that the user was not found
        print(f"User with name {user_name} does not exist.")

# View all products for a given tag
def view_products_by_tag(tag_name):
    # Print a message indicating that we're viewing products with the given tag
    print(f"Viewing products with tag {tag_name}")
    
    try:
        # Get the tag object from the database based on the given tag name
        tag = Tags.get(Tags.name == tag_name)
        
        # Query the product_tags table to get all product-tag relationships that have the given tag
        query = ProductTags.select().where(ProductTags.tag == tag)
        
        # Loop through each product-tag relationship in the query results
        for product_tag in query:
            # Get the product object that corresponds to the current product-tag relationship
            product = Products.get(Products.id == product_tag.product_id)
            
            # Print the name of the product
            print(product.name)
    
    except Tags.DoesNotExist:
        # If the tag does not exist, print a message indicating that the tag was not found
        print(f"Tag with name {tag_name} does not exist.")

# Remove a product from a user
def remove_product_from_user(user_name, product_name):
    # Print a message indicating that we're removing the product from the user
    print(f"Removing product {product_name} from user {user_name}")
    
    try:
        # Get the user object from the database based on the given user name
        user = Users.get(Users.name == user_name)
        
        # Get the product object from the database based on the given product name
        product = Products.get(Products.name == product_name)
        
        # Query the transactions table to get the transaction object that represents the purchase of the product by the user
        transaction = Transactions.select().where(Transactions.buyer == user, Transactions.product == product).first()
        
        if transaction:
            # If the transaction exists, get the quantity of the product that was purchased by the user
            quantity = transaction.quantity
            
            # Delete the transaction from the database
            transaction.delete_instance()
            
            # Print a message indicating how much of the product was removed from the user
            print(f"Removed {quantity} of product {product_name} from user {user_name}")
        else:
            # If the transaction does not exist, print a message indicating that the user does not have the product
            print(f"User {user_name} does not have product {product_name}")
    
    except Users.DoesNotExist:
        # If the user does not exist, print a message indicating that the user was not found
        print(f"User with name {user_name} does not exist.")
    
    except Products.DoesNotExist:
        # If the product does not exist, print a message indicating that the product was not found
        print(f"Product with name {product_name} does not exist.")

# Update the stock quantity of a product by name
def update_product_quantity(product_name, new_quantity):
    # Print a message indicating that we're updating the quantity of the product
    print(f"Updating quantity of product {product_name} by {new_quantity}")
    
    try:
        # Get the product object from the database based on the given product name
        product = Products.get(Products.name == product_name)
        
        # Add the new quantity to the current quantity of the product
        product.quantity += new_quantity
        
        # Save the updated product object to the database
        product.save()
        
        # Print a message indicating the new quantity of the product
        print(f"Updated quantity of product {product_name} to {product.quantity}")
    
    except Products.DoesNotExist:
        # If the product does not exist, print a message indicating that the product was not found
        print(f"Product with name {product_name} does not exist.")

# Handle a purchase of a product by a user
def handle_purchase(buyer_name, product_name, quantity):
    # Print a message indicating that we're handling the purchase
    print(f"Handling purchase of {quantity} of product {product_name} by {buyer_name}")
    
    try:
        # Get the user object from the database based on the given user name
        buyer = Users.get(Users.name == buyer_name)
        
        # Get the product object from the database based on the given product name
        product = Products.get(Products.name == product_name)
        
        # Check if there is enough stock of the product for the purchase
        if product.quantity < quantity:
            print(f"Not enough stock for product {product_name}")
            return
        
        # Check if the user has already purchased the product before
        transaction = Transactions.select().where(Transactions.buyer == buyer, Transactions.product == product).first()
        
        if transaction:
            # If the user has already purchased the product, update the quantity of the existing transaction
            transaction.quantity += quantity
            transaction.save()
        else:
            # If the user has not purchased the product before, create a new transaction
            Transactions.create(buyer=buyer, product=product, quantity=quantity)
        
        # Update the stock quantity of the product
        product.quantity -= quantity
        product.save()
        
        # Print a message indicating that the purchase was completed
        print(f"Purchase of {quantity} of product {product_name} by {buyer_name} completed.")
        
        # Get the quantity of the product that the user has purchased
        user_product_count = Transactions.select().where(Transactions.buyer == buyer, Transactions.product == product).first().quantity
        
        # Determine whether to use singular or plural form of the product name based on the quantity purchased
        if user_product_count > 1:
            plural = "s"
        else:
            plural = ""
        
        # Print a message indicating how much of the product the user now has
        print(f"User {buyer_name} now has {user_product_count} {product_name}{plural}.")
    
    except Users.DoesNotExist:
        # If the user does not exist, print a message indicating that the user was not found
        print(f"User with name {buyer_name} does not exist.")
    
    except Products.DoesNotExist:
        # If the product does not exist, print a message indicating that the product was not found
        print(f"Product with name {product_name} does not exist.")

if __name__ == "__main__":
    main()