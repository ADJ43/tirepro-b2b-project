import math
import random
from datetime import datetime, timezone
from decimal import Decimal
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, joinedload
from ..database import get_db
from ..models import Order, OrderItem, Product
from ..schemas import OrderCreate, OrderOut, OrderItemOut, ProductOut, OrderListResponse
from ..fefo import select_fefo_inventory, get_age_category, get_discount_percent

router = APIRouter(prefix="/api/orders", tags=["Orders"])


def _generate_order_number() -> str:
    year = datetime.now(timezone.utc).year
    seq = random.randint(10000, 99999)
    return f"TP-{year}-{seq}"


def _product_to_out(p: Product) -> ProductOut:
    age_cat = p.age_category
    return ProductOut(
        id=p.id, sku=p.sku, name=p.name,
        brand_id=p.brand_id, category_id=p.category_id,
        brand_name=p.brand.name if p.brand else "",
        category_name=p.category.name if p.category else "",
        tire_size=p.tire_size, load_index=p.load_index,
        speed_rating=p.speed_rating, tire_type=p.tire_type,
        description=p.description, wholesale_price=p.wholesale_price,
        msrp=p.msrp, stock_quantity=p.stock_quantity,
        warehouse_location=p.warehouse_location,
        image_url=p.image_url,
        dot_code=p.dot_code,
        manufacture_date=p.manufacture_date,
        age_category=age_cat,
        effective_price=p.effective_price,
        discount_percent=get_discount_percent(age_cat),
        is_active=p.is_active,
        created_at=p.created_at, updated_at=p.updated_at,
    )


def _order_to_out(order: Order) -> OrderOut:
    return OrderOut(
        id=order.id,
        order_number=order.order_number,
        dealer_name=order.dealer_name,
        dealer_email=order.dealer_email,
        status=order.status,
        subtotal=order.subtotal,
        tax=order.tax,
        total=order.total,
        notes=order.notes,
        created_at=order.created_at,
        items=[
            OrderItemOut(
                id=item.id,
                product_id=item.product_id,
                quantity=item.quantity,
                unit_price=item.unit_price,
                line_total=item.line_total,
                warehouse_source=item.warehouse_source,
                age_category=item.age_category,
                discount_percent=item.discount_percent or 0,
                product=_product_to_out(item.product) if item.product else None,
            )
            for item in order.items
        ],
    )


@router.post("", response_model=OrderOut, status_code=201)
def create_order(payload: OrderCreate, db: Session = Depends(get_db)):
    """
    Create an order using FEFO (First Expired, First Out) allocation.
    For each line item, the system finds all warehouse variants of the
    same tire and allocates from the oldest stock first.
    """
    subtotal = Decimal("0.00")
    order_items = []

    for item in payload.items:
        # Verify the product exists
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail=f"Product {item.product_id} not found")

        # Use FEFO to allocate across warehouses
        try:
            allocations = select_fefo_inventory(db, item.product_id, item.quantity)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

        # Create order items for each FEFO allocation
        for alloc in allocations:
            line_total = alloc["unit_price"] * alloc["quantity"]
            subtotal += line_total

            order_items.append(
                OrderItem(
                    product_id=alloc["product_id"],
                    quantity=alloc["quantity"],
                    unit_price=alloc["unit_price"],
                    line_total=line_total,
                    warehouse_source=alloc["warehouse"],
                    age_category=alloc["age_category"],
                    discount_percent=alloc["discount_percent"],
                )
            )

    tax = (subtotal * Decimal("0.07")).quantize(Decimal("0.01"))
    total = subtotal + tax

    order = Order(
        order_number=_generate_order_number(),
        dealer_name=payload.dealer_name,
        dealer_email=payload.dealer_email,
        notes=payload.notes,
        subtotal=subtotal,
        tax=tax,
        total=total,
    )
    order.items = order_items

    db.add(order)
    db.commit()
    db.refresh(order)

    # Reload with relationships
    order = (
        db.query(Order)
        .options(joinedload(Order.items).joinedload(OrderItem.product))
        .filter(Order.id == order.id)
        .first()
    )
    return _order_to_out(order)


@router.get("", response_model=OrderListResponse)
def list_orders(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    query = db.query(Order).options(joinedload(Order.items).joinedload(OrderItem.product))
    total = db.query(Order).count()
    total_pages = math.ceil(total / per_page) if total > 0 else 1

    orders = (
        query.order_by(Order.created_at.desc())
        .offset((page - 1) * per_page)
        .limit(per_page)
        .all()
    )

    return OrderListResponse(
        items=[_order_to_out(o) for o in orders],
        total=total,
        page=page,
        per_page=per_page,
        total_pages=total_pages,
    )


@router.get("/{order_number}", response_model=OrderOut)
def get_order(order_number: str, db: Session = Depends(get_db)):
    order = (
        db.query(Order)
        .options(joinedload(Order.items).joinedload(OrderItem.product))
        .filter(Order.order_number == order_number)
        .first()
    )
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return _order_to_out(order)
