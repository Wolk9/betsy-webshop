# Models go here
from peewee import Model, CharField, DecimalField, IntegerField, ForeignKeyField
from peewee import SqliteDatabase

# Initialize the database
db = SqliteDatabase('betsy.db')

class BaseModel(Model):
    class Meta:
        database = db

# User model
class Users(BaseModel):
    name = CharField()
    address = CharField()
    billing_info = CharField()

# Tag model
class Tags(BaseModel):
    name = CharField(unique=True)

# Product model
class Products(BaseModel):
    name = CharField()
    description = CharField()
    price = DecimalField(decimal_places=2)  # Safeguard against rounding errors
    quantity = IntegerField()


    class Meta:
        indexes = (
            (('name', 'description'), True),  # Enabling indexing for faster queries
        )

# Product-Tag Relationship
class ProductTags(BaseModel):
    product = ForeignKeyField(Products, backref='tags')
    tag = ForeignKeyField(Tags, backref='products')

# Transaction model
class Transactions(BaseModel):
    buyer = ForeignKeyField(Users, backref='transactions')
    product = ForeignKeyField(Products, backref='transactions')
    quantity = IntegerField()

# Create tables
def init_database():
    db.connect()
    db.create_tables([Users, Tags, Products, ProductTags, Transactions])
