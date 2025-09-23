from datetime import datetime
from peewee import (
    Model,
    SqliteDatabase,
    AutoField,
    CharField,
    DateTimeField,
    ForeignKeyField,
    TextField,
    BooleanField,
    DecimalField,
    IntegerField,
)
from playhouse.shortcuts import model_to_dict
from config.config import db_config

db = SqliteDatabase(db_config.DB_PATH)

class BaseModel(Model):
    class Meta:
        database = db

class Role(BaseModel):
    id = AutoField()
    name = CharField(unique=True)

class Tier(BaseModel):
    id = AutoField()
    name = CharField(unique=True)
    price = DecimalField(max_digits=10, decimal_places=2)
    description = TextField(null=True)

class UserSubscription(BaseModel):
    id = AutoField()
    tier = ForeignKeyField(Tier, backref="subscriptions", null=False)
    active = BooleanField(default=True)
    started_at = DateTimeField(default=datetime.utcnow)
    end_at = DateTimeField(null=True)

class User(BaseModel):
    id = CharField(primary_key=True)
    name = CharField()
    email = CharField(unique=True)
    phone_number = CharField(null=True)
    avatar_url = TextField(null=True)
    created_at = DateTimeField(default=datetime.utcnow)
    subscription = ForeignKeyField(UserSubscription, backref="user", null=True, unique=True)

    def to_dict(self, backrefs=True):
        return model_to_dict(self, backrefs=backrefs)

class Car(BaseModel):
    id = AutoField()
    owner = ForeignKeyField(User, backref="cars")
    brand = CharField()
    model = CharField()
    license_plate = CharField(unique=True)
    color = CharField(null=True)
    
class Transaction(BaseModel):
    id = AutoField()
    user = ForeignKeyField(User, backref="transactions")
    amount = DecimalField(max_digits=10, decimal_places=2)
    timestamp = DateTimeField(default=datetime.utcnow)
    description = TextField(null=True)
    status = CharField(default="pending")  # e.g., pending, completed, failed

# Many-to-many through table for User <-> Role
class UserRole(BaseModel):
    id = AutoField()
    user = ForeignKeyField(User, backref="user_roles")
    role = ForeignKeyField(Role, backref="role_users")

class Parking(BaseModel):
    id = AutoField()
    location = CharField()
    latitude = DecimalField(max_digits=9, decimal_places=6)
    longitude = DecimalField(max_digits=9, decimal_places=6)
    capacity = IntegerField() # TODO Ask Rostik if we need it
    created_at = DateTimeField(default=datetime.utcnow)

class Parking_Lot:
    id = AutoField()
    status = CharField(default="free")  # e.g., taken, free
    timestamp = DateTimeField(default=datetime.utcnow)
    parking = ForeignKeyField(Parking, backref="parking_lots")




def init_db():
    db.connect(reuse_if_open=True)
    db.create_tables([Role, UserSubscription, User, Car, Transaction, UserRole])
    db.close()
