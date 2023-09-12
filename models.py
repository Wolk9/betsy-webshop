# Models go here
from peewee import Model, CharField, DecimalField, IntegerField, ForeignKeyField
from peewee import SqliteDatabase

# Initialize the database
db = SqliteDatabase('betsy.db')

class BaseModel(Model):
    class Meta:
        database = db

# User model
class User(BaseModel):
    name = CharField()
    address = CharField()
    billing_info = CharField()

# Tag model
class Tag(BaseModel):
    name = CharField(unique=True)

# Product model
class Product(BaseModel):
    name = CharField()
    description = CharField()
    price = DecimalField(decimal_places=2)  # Safeguard against rounding errors
    quantity = IntegerField()
    owner = ForeignKeyField(User, backref='products')

    class Meta:
        indexes = (
            (('name', 'description'), True),  # Enabling indexing for faster queries
        )

# Product-Tag Relationship
class ProductTag(BaseModel):
    product = ForeignKeyField(Product, backref='tags')
    tag = ForeignKeyField(Tag, backref='products')

# Transaction model
class Transaction(BaseModel):
    buyer = ForeignKeyField(User, backref='transactions')
    product = ForeignKeyField(Product, backref='transactions')
    quantity = IntegerField()

# Create tables
db.connect()
db.create_tables([User, Tag, Product, ProductTag, Transaction])
