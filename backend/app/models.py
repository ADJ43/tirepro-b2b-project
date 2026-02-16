from datetime import date, datetime, timezone
from decimal import Decimal
from sqlalchemy import (
    Column, Integer, String, Text, Numeric, Boolean, DateTime, Date,
    ForeignKey, Index
)
from sqlalchemy.orm import relationship
from .database import Base


class Brand(Base):
    __tablename__ = "brands"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False, index=True)
    slug = Column(String(120), unique=True, nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    products = relationship("Product", back_populates="brand")


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False, index=True)
    slug = Column(String(120), unique=True, nullable=False)
    description = Column(Text, nullable=True)

    products = relationship("Product", back_populates="category")


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    sku = Column(String(50), unique=True, nullable=False, index=True)
    name = Column(String(200), nullable=False)
    brand_id = Column(Integer, ForeignKey("brands.id"), nullable=False, index=True)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False, index=True)
    tire_size = Column(String(50), nullable=False)
    load_index = Column(String(10), nullable=True)
    speed_rating = Column(String(5), nullable=True)
    tire_type = Column(String(50), nullable=True)
    description = Column(Text, nullable=True)
    wholesale_price = Column(Numeric(10, 2), nullable=False)
    msrp = Column(Numeric(10, 2), nullable=True)
    stock_quantity = Column(Integer, default=0)
    warehouse_location = Column(String(100), nullable=True)
    image_url = Column(String(500), nullable=True)
    dot_code = Column(String(4), nullable=True)
    manufacture_date = Column(Date, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    brand = relationship("Brand", back_populates="products")
    category = relationship("Category", back_populates="products")

    @property
    def age_years(self) -> float:
        if not self.manufacture_date:
            return 0.0
        return (date.today() - self.manufacture_date).days / 365.25

    @property
    def age_category(self) -> str:
        years = self.age_years
        if years < 2:
            return "fresh"
        elif years < 4:
            return "normal"
        elif years < 5:
            return "aging"
        elif years < 6:
            return "old"
        return "critical"

    @property
    def age_discount_multiplier(self) -> Decimal:
        cat = self.age_category
        if cat == "aging":
            return Decimal("0.90")
        elif cat == "old":
            return Decimal("0.80")
        elif cat == "critical":
            return Decimal("0.70")
        return Decimal("1.00")

    @property
    def effective_price(self) -> Decimal:
        return (self.wholesale_price * self.age_discount_multiplier).quantize(Decimal("0.01"))


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    order_number = Column(String(20), unique=True, nullable=False, index=True)
    dealer_name = Column(String(200), nullable=False)
    dealer_email = Column(String(200), nullable=False)
    status = Column(String(20), default="pending")
    subtotal = Column(Numeric(10, 2), nullable=False)
    tax = Column(Numeric(10, 2), nullable=False)
    total = Column(Numeric(10, 2), nullable=False)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")


class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id", ondelete="CASCADE"), nullable=False, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Numeric(10, 2), nullable=False)
    line_total = Column(Numeric(10, 2), nullable=False)
    warehouse_source = Column(String(100), nullable=True)
    age_category = Column(String(20), nullable=True)
    discount_percent = Column(Integer, default=0)

    order = relationship("Order", back_populates="items")
    product = relationship("Product")
