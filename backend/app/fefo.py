"""
FEFO (First Expired, First Out) Inventory Management

Tire industry rules:
- DOT date code: 4-digit "WWYY" (week of year + 2-digit year)
- Fresh: < 2 years from manufacture — full price
- Normal: 2-4 years — full price, but ship before aging tires
- Aging: 4-5 years — 10% discount, prioritize shipping
- Old: 5-6 years — 20% discount, should be cleared
- Critical: 6+ years — 30% discount, industry recommends replacement

FEFO logic: When a dealer orders tires, allocate from the OLDEST
available stock first (across all warehouses) to prevent waste.
"""

from datetime import date
from decimal import Decimal
from sqlalchemy.orm import Session
from .models import Product


# ---------------------------------------------------------------------------
# Age helpers
# ---------------------------------------------------------------------------

def get_age_years(manufacture_date: date) -> float:
    """Calculate age in years from manufacture date."""
    if not manufacture_date:
        return 0.0
    return (date.today() - manufacture_date).days / 365.25


def get_age_category(manufacture_date: date) -> str:
    """Return age bucket: fresh, normal, aging, old, critical."""
    years = get_age_years(manufacture_date)
    if years < 2:
        return "fresh"
    elif years < 4:
        return "normal"
    elif years < 5:
        return "aging"
    elif years < 6:
        return "old"
    return "critical"


def get_discount_multiplier(age_category: str) -> Decimal:
    """Return price multiplier based on age category."""
    return {
        "fresh": Decimal("1.00"),
        "normal": Decimal("1.00"),
        "aging": Decimal("0.90"),   # 10% off
        "old": Decimal("0.80"),     # 20% off
        "critical": Decimal("0.70"),  # 30% off
    }.get(age_category, Decimal("1.00"))


def get_discount_percent(age_category: str) -> int:
    """Return discount percentage as int (0, 10, 20, 30)."""
    return {
        "fresh": 0,
        "normal": 0,
        "aging": 10,
        "old": 20,
        "critical": 30,
    }.get(age_category, 0)


# ---------------------------------------------------------------------------
# FEFO Inventory Selection
# ---------------------------------------------------------------------------

def select_fefo_inventory(db: Session, product_id: int, quantity: int) -> list[dict]:
    """
    Given a product ID, find all warehouse variants of the same tire
    (matching by name + tire_size) and allocate the requested quantity
    using FEFO — oldest manufacture_date first.

    Returns a list of allocation dicts:
    [
        {
            "product_id": int,
            "warehouse": str,
            "quantity": int,
            "unit_price": Decimal,     # effective (discounted) price
            "base_price": Decimal,     # original wholesale price
            "age_category": str,
            "discount_percent": int,
            "dot_code": str,
            "manufacture_date": date,
        },
        ...
    ]

    Raises ValueError if total available stock is insufficient.
    """
    # Get the requested product to find its name + tire_size
    target = db.query(Product).filter(Product.id == product_id).first()
    if not target:
        raise ValueError(f"Product {product_id} not found")

    # Find all variants: same product name + tire_size, active, in stock
    variants = (
        db.query(Product)
        .filter(
            Product.name == target.name,
            Product.tire_size == target.tire_size,
            Product.is_active == True,
            Product.stock_quantity > 0,
        )
        .order_by(Product.manufacture_date.asc().nullslast())
        .all()
    )

    total_available = sum(v.stock_quantity for v in variants)
    if total_available < quantity:
        raise ValueError(
            f"Insufficient stock for {target.name} ({target.tire_size}). "
            f"Available: {total_available}, Requested: {quantity}"
        )

    # Allocate oldest-first (FEFO)
    allocations = []
    remaining = quantity

    for variant in variants:
        if remaining <= 0:
            break

        alloc_qty = min(remaining, variant.stock_quantity)
        age_cat = variant.age_category
        discount_pct = get_discount_percent(age_cat)
        multiplier = get_discount_multiplier(age_cat)
        effective_price = (variant.wholesale_price * multiplier).quantize(Decimal("0.01"))

        allocations.append({
            "product_id": variant.id,
            "warehouse": variant.warehouse_location,
            "quantity": alloc_qty,
            "unit_price": effective_price,
            "base_price": variant.wholesale_price,
            "age_category": age_cat,
            "discount_percent": discount_pct,
            "dot_code": variant.dot_code,
            "manufacture_date": variant.manufacture_date,
        })

        # Decrement stock on this variant
        variant.stock_quantity -= alloc_qty
        remaining -= alloc_qty

    return allocations
