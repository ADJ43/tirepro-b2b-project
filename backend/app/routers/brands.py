from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Brand, Product
from ..schemas import BrandOut

router = APIRouter(prefix="/api/brands", tags=["Brands"])


@router.get("", response_model=list[BrandOut])
def list_brands(db: Session = Depends(get_db)):
    results = (
        db.query(Brand, func.count(Product.id).label("product_count"))
        .outerjoin(Product, Product.brand_id == Brand.id)
        .group_by(Brand.id)
        .order_by(Brand.name)
        .all()
    )
    return [
        BrandOut(
            id=brand.id,
            name=brand.name,
            slug=brand.slug,
            description=brand.description,
            product_count=count,
        )
        for brand, count in results
    ]
