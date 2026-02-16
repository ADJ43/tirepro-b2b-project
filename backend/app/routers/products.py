import math
from datetime import date
from decimal import Decimal
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func, text, literal_column
from sqlalchemy.orm import Session, joinedload
from ..database import get_db
from ..models import Product, Brand, Category
from ..schemas import (
    ProductOut, ProductListResponse, FacetItem, PriceRangeFacet,
    FacetsResponse, WarehouseInventory,
)
from ..fefo import get_age_category, get_discount_percent, get_discount_multiplier

router = APIRouter(prefix="/api/products", tags=["Products"])


def _product_to_out(p: Product) -> ProductOut:
    age_cat = p.age_category
    disc_pct = get_discount_percent(age_cat)
    return ProductOut(
        id=p.id,
        sku=p.sku,
        name=p.name,
        brand_id=p.brand_id,
        category_id=p.category_id,
        brand_name=p.brand.name if p.brand else "",
        category_name=p.category.name if p.category else "",
        tire_size=p.tire_size,
        load_index=p.load_index,
        speed_rating=p.speed_rating,
        tire_type=p.tire_type,
        description=p.description,
        wholesale_price=p.wholesale_price,
        msrp=p.msrp,
        stock_quantity=p.stock_quantity,
        warehouse_location=p.warehouse_location,
        image_url=p.image_url,
        dot_code=p.dot_code,
        manufacture_date=p.manufacture_date,
        age_category=age_cat,
        effective_price=p.effective_price,
        discount_percent=disc_pct,
        is_active=p.is_active,
        created_at=p.created_at,
        updated_at=p.updated_at,
    )


def _apply_base_filters(query, search, brand_id, category_id, min_price,
                          max_price, in_stock, tire_size, tire_type):
    """Apply common filters to a query (reused by list + facets)."""
    query = query.filter(Product.is_active == True)

    if brand_id:
        query = query.filter(Product.brand_id == brand_id)
    if category_id:
        query = query.filter(Product.category_id == category_id)
    if min_price is not None:
        query = query.filter(Product.wholesale_price >= min_price)
    if max_price is not None:
        query = query.filter(Product.wholesale_price <= max_price)
    if in_stock:
        query = query.filter(Product.stock_quantity > 0)
    if tire_size:
        query = query.filter(Product.tire_size == tire_size)
    if tire_type:
        query = query.filter(Product.tire_type == tire_type)

    if search:
        ts_vector = func.to_tsvector(
            literal_column("'english'"),
            func.coalesce(Product.name, "") + " " +
            func.coalesce(Product.tire_size, "") + " " +
            func.coalesce(Product.description, "")
        )
        ts_query = func.plainto_tsquery(literal_column("'english'"), search)
        query = query.filter(ts_vector.op("@@")(ts_query))

    return query


# ---- Facets endpoint (must be BEFORE /{product_id} to avoid route conflict) ----

@router.get("/facets", response_model=FacetsResponse)
def get_facets(
    search: Optional[str] = None,
    brand_id: Optional[int] = None,
    category_id: Optional[int] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    in_stock: Optional[bool] = None,
    tire_size: Optional[str] = None,
    tire_type: Optional[str] = None,
    db: Session = Depends(get_db),
):
    """
    Returns facet counts for each filter dimension.
    Each facet is computed with ALL OTHER active filters applied,
    but NOT the filter for that specific dimension.
    """

    def base_q():
        return db.query(Product).filter(Product.is_active == True)

    def apply_search(q):
        if search:
            ts_vector = func.to_tsvector(
                literal_column("'english'"),
                func.coalesce(Product.name, "") + " " +
                func.coalesce(Product.tire_size, "") + " " +
                func.coalesce(Product.description, "")
            )
            ts_query = func.plainto_tsquery(literal_column("'english'"), search)
            q = q.filter(ts_vector.op("@@")(ts_query))
        return q

    def apply_common(q, skip_field=None):
        """Apply all filters except the one named by skip_field."""
        q = apply_search(q)
        if brand_id and skip_field != "brand":
            q = q.filter(Product.brand_id == brand_id)
        if category_id and skip_field != "category":
            q = q.filter(Product.category_id == category_id)
        if min_price is not None and skip_field != "price":
            q = q.filter(Product.wholesale_price >= min_price)
        if max_price is not None and skip_field != "price":
            q = q.filter(Product.wholesale_price <= max_price)
        if in_stock and skip_field != "stock":
            q = q.filter(Product.stock_quantity > 0)
        if tire_size and skip_field != "tire_size":
            q = q.filter(Product.tire_size == tire_size)
        if tire_type and skip_field != "tire_type":
            q = q.filter(Product.tire_type == tire_type)
        return q

    # Brand facets
    brand_q = apply_common(base_q(), skip_field="brand")
    brand_counts = (
        brand_q.join(Brand)
        .with_entities(Brand.id, Brand.name, func.count(Product.id))
        .group_by(Brand.id, Brand.name)
        .order_by(Brand.name)
        .all()
    )
    brand_facets = [FacetItem(id=bid, name=bname, count=cnt) for bid, bname, cnt in brand_counts]

    # Category facets
    cat_q = apply_common(base_q(), skip_field="category")
    cat_counts = (
        cat_q.join(Category)
        .with_entities(Category.id, Category.name, func.count(Product.id))
        .group_by(Category.id, Category.name)
        .order_by(Category.name)
        .all()
    )
    cat_facets = [FacetItem(id=cid, name=cname, count=cnt) for cid, cname, cnt in cat_counts]

    # Tire size facets
    size_q = apply_common(base_q(), skip_field="tire_size")
    size_counts = (
        size_q.with_entities(Product.tire_size, func.count(Product.id))
        .group_by(Product.tire_size)
        .order_by(Product.tire_size)
        .all()
    )
    size_facets = [FacetItem(value=sz, count=cnt) for sz, cnt in size_counts]

    # Tire type facets
    type_q = apply_common(base_q(), skip_field="tire_type")
    type_counts = (
        type_q.with_entities(Product.tire_type, func.count(Product.id))
        .filter(Product.tire_type.isnot(None))
        .group_by(Product.tire_type)
        .order_by(Product.tire_type)
        .all()
    )
    type_facets = [FacetItem(value=tt, count=cnt) for tt, cnt in type_counts]

    # Age category facets (computed in Python since age is derived)
    age_q = apply_common(base_q(), skip_field=None)
    all_products_for_age = age_q.with_entities(Product.manufacture_date).all()
    age_buckets = {}
    for (mfg_date,) in all_products_for_age:
        cat = get_age_category(mfg_date) if mfg_date else "fresh"
        age_buckets[cat] = age_buckets.get(cat, 0) + 1
    age_order = ["fresh", "normal", "aging", "old", "critical"]
    age_facets = [
        FacetItem(value=cat, count=age_buckets.get(cat, 0))
        for cat in age_order
        if age_buckets.get(cat, 0) > 0
    ]

    # Price range facets
    price_q = apply_common(base_q(), skip_field="price")
    price_ranges_def = [
        ("Under $75", 0, 75),
        ("$75 - $150", 75, 150),
        ("$150 - $250", 150, 250),
        ("$250+", 250, None),
    ]
    price_facets = []
    for label, pmin, pmax in price_ranges_def:
        pq = price_q
        pq = pq.filter(Product.wholesale_price >= pmin)
        if pmax is not None:
            pq = pq.filter(Product.wholesale_price < pmax)
        cnt = pq.count()
        price_facets.append(PriceRangeFacet(
            label=label, min_val=pmin, max_val=pmax, count=cnt
        ))

    return FacetsResponse(
        brands=brand_facets,
        categories=cat_facets,
        tire_sizes=size_facets,
        tire_types=type_facets,
        age_categories=age_facets,
        price_ranges=price_facets,
    )


# ---- Warehouse inventory for a product (by name+size) ----

@router.get("/inventory/{product_id}", response_model=list[WarehouseInventory])
def get_inventory(product_id: int, db: Session = Depends(get_db)):
    """Get all warehouse variants of a product for FEFO display."""
    target = db.query(Product).filter(Product.id == product_id).first()
    if not target:
        raise HTTPException(status_code=404, detail="Product not found")

    variants = (
        db.query(Product)
        .filter(
            Product.name == target.name,
            Product.tire_size == target.tire_size,
            Product.is_active == True,
        )
        .order_by(Product.manufacture_date.asc().nullslast())
        .all()
    )

    result = []
    for i, v in enumerate(variants):
        age_cat = v.age_category
        result.append(WarehouseInventory(
            product_id=v.id,
            warehouse=v.warehouse_location or "Unknown",
            stock_quantity=v.stock_quantity,
            dot_code=v.dot_code,
            manufacture_date=v.manufacture_date,
            age_category=age_cat,
            effective_price=v.effective_price,
            discount_percent=get_discount_percent(age_cat),
            ships_first=(i == 0 and v.stock_quantity > 0),
        ))

    return result


# ---- Product listing ----

@router.get("", response_model=ProductListResponse)
def list_products(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    brand_id: Optional[int] = None,
    category_id: Optional[int] = None,
    search: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    in_stock: Optional[bool] = None,
    tire_size: Optional[str] = None,
    tire_type: Optional[str] = None,
    age_category: Optional[str] = None,
    sort_by: Optional[str] = Query(None, pattern="^(price|name|created_at|age)$"),
    sort_order: Optional[str] = Query("asc", pattern="^(asc|desc)$"),
    db: Session = Depends(get_db),
):
    query = db.query(Product).options(joinedload(Product.brand), joinedload(Product.category))
    query = _apply_base_filters(
        query, search, brand_id, category_id,
        min_price, max_price, in_stock, tire_size, tire_type
    )

    # Age category filter (must be done in Python since it's derived)
    # For efficiency with large datasets you'd use a DB column, but for demo this works
    if age_category:
        # Get all matching IDs first, then filter
        all_q = db.query(Product.id, Product.manufacture_date)
        all_q = _apply_base_filters(
            all_q, search, brand_id, category_id,
            min_price, max_price, in_stock, tire_size, tire_type
        )
        matching_ids = [
            pid for pid, mdate in all_q.all()
            if get_age_category(mdate) == age_category
        ]
        query = query.filter(Product.id.in_(matching_ids))

    # Sorting
    if sort_by == "price":
        col = Product.wholesale_price
    elif sort_by == "name":
        col = Product.name
    elif sort_by == "age":
        col = Product.manufacture_date
    else:
        col = Product.created_at

    if sort_order == "desc":
        query = query.order_by(col.desc())
    else:
        query = query.order_by(col.asc())

    total = query.count()
    total_pages = math.ceil(total / per_page) if total > 0 else 1
    items = query.offset((page - 1) * per_page).limit(per_page).all()

    return ProductListResponse(
        items=[_product_to_out(p) for p in items],
        total=total,
        page=page,
        per_page=per_page,
        total_pages=total_pages,
    )


@router.get("/{product_id}", response_model=ProductOut)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = (
        db.query(Product)
        .options(joinedload(Product.brand), joinedload(Product.category))
        .filter(Product.id == product_id)
        .first()
    )
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return _product_to_out(product)
