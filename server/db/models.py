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
from sqlalchemy.orm import declarative_base, relationship, sessionmaker, scoped_session
from config.config import db_config

engine = create_engine(db_config.DB_CONNECTION, echo=False, future=True)
SessionLocal = scoped_session(
    sessionmaker(bind=engine, autoflush=False, autocommit=False)
)
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
    subscription_id = Column(
        Integer, ForeignKey("user_subscription.id"), unique=True, nullable=True
    )
    subscription = relationship(
        "UserSubscription", back_populates="user", uselist=False
    )
    cars = relationship("Car", back_populates="owner", cascade="all, delete-orphan")
    transactions = relationship("Transaction", back_populates="user")
    user_roles = relationship(
        "UserRole", back_populates="user", cascade="all, delete-orphan"
    )
    bookings = relationship(
        "Booking", back_populates="user", cascade="all, delete-orphan"
    )

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "phoneNumber": self.phone_number,
            "avatarUrl": self.avatar_url,
            "createdAt": self.created_at,
        }

    def has_role(self, role_name):
        return any(user_role.role.name == role_name for user_role in self.user_roles)

    def get_roles(self):
        return [user_role.role.name for user_role in self.user_roles]

    def get_cars(self):
        return [car.to_dict() for car in self.cars]

    def get_transactions(self):
        return [transaction.to_dict() for transaction in self.transactions]

    def get_all_info(self):
        user_dict = self.to_dict()
        user_dict["roles"] = self.get_roles()
        user_dict["cars"] = self.get_cars()
        user_dict["transactions"] = self.get_transactions()
        if self.subscription:
            user_dict["subscription"] = {
                "id": self.subscription.id,
                "tier": {
                    "id": self.subscription.tier.id,
                    "name": self.subscription.tier.name,
                    "price": float(self.subscription.tier.price),
                    "description": self.subscription.tier.description,
                },
                "active": self.subscription.active,
                "started_at": self.subscription.started_at,
                "end_at": self.subscription.end_at,
            }
        else:
            user_dict["subscription"] = None
        return user_dict


class Car(Base):
    __tablename__ = "car"
    id = Column(Integer, primary_key=True, autoincrement=True)
    owner_id = Column(String, ForeignKey("user.id"), nullable=False)
    brand = Column(String, nullable=False)
    model = Column(String, nullable=False)
    license_plate = Column(String, unique=True, nullable=False)
    color = Column(String, nullable=True)

    owner = relationship("User", back_populates="cars")
    bookings = relationship(
        "Booking", back_populates="car", cascade="all, delete-orphan"
    )  # <-- змінив з 'booking' на 'bookings' та додав cascade

    def to_dict(self):
        return {
            "id": self.id,
            "number": self.license_plate,
            "brand": self.brand,
            "model": self.model,
            "color": self.color,
        }


class Transaction(Base):
    __tablename__ = "transaction"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String, ForeignKey("user.id"), nullable=False)
    amount = Column(DECIMAL(10, 2), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    description = Column(Text, nullable=True)
    status = Column(String, default="pending")
    user = relationship("User", back_populates="transactions")

    def to_dict(self):
        return {
            "id": self.id,
            "date": self.timestamp,
            "description": self.description,
            "amount": self.amount,
            "status": self.status,
        }


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
    name = Column(String, nullable=False, default="Default Parking")
    location = Column(String, nullable=False)
    latitude = Column(DECIMAL(9, 6), nullable=False)
    longitude = Column(DECIMAL(9, 6), nullable=False)
    capacity = Column(Integer, nullable=False)
    available_spots = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

    parking_lots = relationship("ParkingLot", back_populates="parking", cascade="all, delete-orphan")
    bookings = relationship(
        "Booking", back_populates="parking", cascade="all, delete-orphan"
    )  # <-- перевірено, має ForeignKey в Booking

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "address": self.location,
            "coordinates": {
                "lat": float(self.latitude),
                "lng": float(self.longitude),
            },
            "availableSpots": self.available_spots,
            "totalSpots": len(self.parking_lots),
        }

    def update_available_spots(self):
        self.available_spots = sum(
            1 for lot in self.parking_lots if lot.status == "free"
        )


class ParkingLot(Base):
    __tablename__ = "parking_lot"
    id = Column(Integer, primary_key=True, autoincrement=True)
    status = Column(String, default="free")
    timestamp = Column(DateTime, default=datetime.utcnow)
    parking_id = Column(Integer, ForeignKey("parking.id"), nullable=False)
    parking = relationship("Parking", back_populates="parking_lots")


class Booking(Base):
    __tablename__ = "booking"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String, ForeignKey("user.id"), nullable=False)
    car_id = Column(Integer, ForeignKey("car.id"), nullable=False)
    status = Column(String, nullable=False)
    start = Column(DateTime, nullable=False)
    end = Column(DateTime, nullable=False)
    parking_id = Column(
        Integer, ForeignKey("parking.id"), nullable=False
    )  # <-- додав ForeignKey, щоб join працював

    user = relationship("User", back_populates="bookings")
    car = relationship(
        "Car", back_populates="bookings"
    )  # <-- має відповідати Car.bookings
    parking = relationship(
        "Parking", back_populates="bookings"
    )  # <-- має відповідати Parking.bookings

    def to_dict(self):
        return {
            "id": self.id,
            "userId": self.user_id,
            "carId": self.car_id,
            "parkingId": self.parking_id,
            "status": self.status,
            "start": self.start,
            "end": self.end,
        }


def init_db():
    Base.metadata.create_all(bind=engine)
