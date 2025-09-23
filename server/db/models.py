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
from datetime import datetime
import os

# Simple SQLite database in the server folder
DB_PATH = os.path.join(os.path.dirname(__file__), "app.db")
db = SqliteDatabase(DB_PATH)

class BaseModel(Model):
    class Meta:
        database = db

class Role(BaseModel):
    id = AutoField()
    name = CharField(unique=True)

class UserSubscription(BaseModel):
    id = AutoField()
    plan = CharField()
    active = BooleanField(default=True)
    started_at = DateTimeField(default=datetime.utcnow)

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
    make = CharField()
    model = CharField()
    year = IntegerField(null=True)

class Transaction(BaseModel):
    id = AutoField()
    user = ForeignKeyField(User, backref="transactions")
    amount = DecimalField(max_digits=10, decimal_places=2)
    timestamp = DateTimeField(default=datetime.utcnow)
    description = TextField(null=True)

# Many-to-many through table for User <-> Role
class UserRole(BaseModel):
    id = AutoField()
    user = ForeignKeyField(User, backref="user_roles")
    role = ForeignKeyField(Role, backref="role_users")


def init_db():
    db.connect(reuse_if_open=True)
    db.create_tables([Role, UserSubscription, User, Car, Transaction, UserRole])
    db.close()
