from datetime import date, datetime
from decimal import Decimal
from typing import Optional
from pydantic import BaseModel, Field


# --- Brand ---
class BrandOut(BaseModel):
    id: int
    name: str
    slug: str
    description: Optional[str] = None
    product_count: int = 0

    model_config = {"from_attributes": True}


# --- Category ---
class CategoryOut(BaseModel):
    id: int
    name: str
    slug: str
    description: Optional[str] = None
    product_count: int = 0

    model_config = {"from_attributes": True}


# --- Product ---
class ProductOut(BaseModel):
    id: int
    sku: str
    name: str
    brand_id: int
    category_id: int
    brand_name: str = ""
    category_name: str = ""
    tire_size: str
    load_index: Optional[str] = None
    speed_rating: Optional[str] = None
    tire_type: Optional[str] = None
    description: Optional[str] = None
    wholesale_price: Decimal
    msrp: Optional[Decimal] = None
    stock_quantity: int
    warehouse_location: Optional[str] = None
    image_url: Optional[str] = None
    dot_code: Optional[str] = None
    manufacture_date: Optional[date] = None
    age_category: Optional[str] = None
    effective_price: Optional[Decimal] = None
    discount_percent: int = 0
    is_active: bool
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


class ProductListResponse(BaseModel):
    items: list[ProductOut]
    total: int
    page: int
    per_page: int
    total_pages: int


# --- Faceted Search ---
class FacetItem(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    value: Optional[str] = None
    count: int


class PriceRangeFacet(BaseModel):
    label: str
    min_val: float
    max_val: Optional[float] = None
    count: int


class FacetsResponse(BaseModel):
    brands: list[FacetItem] = []
    categories: list[FacetItem] = []
    tire_sizes: list[FacetItem] = []
    tire_types: list[FacetItem] = []
    age_categories: list[FacetItem] = []
    price_ranges: list[PriceRangeFacet] = []


# --- Warehouse Inventory (for product detail) ---
class WarehouseInventory(BaseModel):
    product_id: int
    warehouse: str
    stock_quantity: int
    dot_code: Optional[str] = None
    manufacture_date: Optional[date] = None
    age_category: str = "fresh"
    effective_price: Decimal
    discount_percent: int = 0
    ships_first: bool = False


# --- Order ---
class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int = Field(gt=0)


class OrderCreate(BaseModel):
    dealer_name: str = Field(min_length=1)
    dealer_email: str = Field(min_length=1)
    notes: Optional[str] = None
    items: list[OrderItemCreate] = Field(min_length=1)


class OrderItemOut(BaseModel):
    id: int
    product_id: int
    quantity: int
    unit_price: Decimal
    line_total: Decimal
    warehouse_source: Optional[str] = None
    age_category: Optional[str] = None
    discount_percent: int = 0
    product: Optional[ProductOut] = None

    model_config = {"from_attributes": True}


class OrderOut(BaseModel):
    id: int
    order_number: str
    dealer_name: str
    dealer_email: str
    status: str
    subtotal: Decimal
    tax: Decimal
    total: Decimal
    notes: Optional[str] = None
    created_at: Optional[datetime] = None
    items: list[OrderItemOut] = []

    model_config = {"from_attributes": True}


class OrderListResponse(BaseModel):
    items: list[OrderOut]
    total: int
    page: int
    per_page: int
    total_pages: int
