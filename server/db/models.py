
from datetime import datetime
from sqlalchemy import (
    create_engine,
    Column,
    String,
    Integer,
    Boolean,
    DateTime,
    Text,
    DECIMAL,
    ForeignKey,
    UniqueConstraint,
)
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from config.config import db_config

engine = create_engine(f"sqlite:///{db_config.DB_PATH}", echo=False, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()

class Role(Base):
    __tablename__ = "role"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)
    role_users = relationship("UserRole", back_populates="role")

class Tier(Base):
    __tablename__ = "tier"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)
    price = Column(DECIMAL(10, 2), nullable=False)
    description = Column(Text, nullable=True)
    subscriptions = relationship("UserSubscription", back_populates="tier")

class UserSubscription(Base):
    __tablename__ = "user_subscription"
    id = Column(Integer, primary_key=True, autoincrement=True)
    tier_id = Column(Integer, ForeignKey("tier.id"), nullable=False)
    active = Column(Boolean, default=True)
    started_at = Column(DateTime, default=datetime.utcnow)
    end_at = Column(DateTime, nullable=True)
    tier = relationship("Tier", back_populates="subscriptions")
    user = relationship("User", back_populates="subscription", uselist=False)

class User(Base):
    __tablename__ = "user"
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone_number = Column(String, nullable=True)
    avatar_url = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    subscription_id = Column(Integer, ForeignKey("user_subscription.id"), unique=True, nullable=True)
    subscription = relationship("UserSubscription", back_populates="user", uselist=False)
    cars = relationship("Car", back_populates="owner")
    transactions = relationship("Transaction", back_populates="user")
    user_roles = relationship("UserRole", back_populates="user")

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class Car(Base):
    __tablename__ = "car"
    id = Column(Integer, primary_key=True, autoincrement=True)
    owner_id = Column(String, ForeignKey("user.id"), nullable=False)
    brand = Column(String, nullable=False)
    model = Column(String, nullable=False)
    license_plate = Column(String, unique=True, nullable=False)
    color = Column(String, nullable=True)
    owner = relationship("User", back_populates="cars")

class Transaction(Base):
    __tablename__ = "transaction"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String, ForeignKey("user.id"), nullable=False)
    amount = Column(DECIMAL(10, 2), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    description = Column(Text, nullable=True)
    status = Column(String, default="pending")
    user = relationship("User", back_populates="transactions")

class UserRole(Base):
    __tablename__ = "user_role"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String, ForeignKey("user.id"), nullable=False)
    role_id = Column(Integer, ForeignKey("role.id"), nullable=False)
    user = relationship("User", back_populates="user_roles")
    role = relationship("Role", back_populates="role_users")

class Parking(Base):
    __tablename__ = "parking"
    id = Column(Integer, primary_key=True, autoincrement=True)
    location = Column(String, nullable=False)
    latitude = Column(DECIMAL(9, 6), nullable=False)
    longitude = Column(DECIMAL(9, 6), nullable=False)
    capacity = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    parking_lots = relationship("ParkingLot", back_populates="parking")

class ParkingLot(Base):
    __tablename__ = "parking_lot"
    id = Column(Integer, primary_key=True, autoincrement=True)
    status = Column(String, default="free")
    timestamp = Column(DateTime, default=datetime.utcnow)
    parking_id = Column(Integer, ForeignKey("parking.id"), nullable=False)
    parking = relationship("Parking", back_populates="parking_lots")

def init_db():
    Base.metadata.create_all(bind=engine)
